import json

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict, JsonResponse
from utils.utils import *
from .models import *
from datetime import timedelta
from backend import settings
from datetime import date, timezone
from utils.utils import *
from utils.responce import *
from utils.params import *
from team.views import create_team_implement


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        username = data_json.get('username')
        password = data_json.get('password')
        email = data_json.get('email')
        nickname = data_json.get('nickname')
        if not nickname:
            nickname = username
        code = data_json.get('code')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'result': 2, 'message': "邮箱已注册!"})
        else:
            if not EmailCode.objects.filter(code=code).exists():
                return JsonResponse({'result': 2, 'message': "验证码错误!"})
            email_code = EmailCode.objects.get(code=code)
            now = datetime.datetime.now(timezone.utc)
            if (now - email_code.time).seconds > 300:
                return JsonResponse({'result': 2, 'message': "验证码已失效!"})
            new_user = User(username=username, nickname=nickname, password= make_password(password), email=email,
                            avatar="http://43.138.77.8:8000/media/image/20220805/20220805223719_68.png")
            new_user.save()
            create_team_implement(new_user, new_user.username + '的团队', '为新用户自动创建')
        return JsonResponse({'result': 0, 'message': "注册成功!"})
    else:
        return JsonResponse({'result': 2, 'message': "前端炸了!"})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        email = data_json.get('email')
        password = data_json.get('password')
        if len(email) == 0 or len(password) == 0:
            result = {'result': 2, 'message': '邮箱与密码不允许为空!'}
        else:
            if not User.objects.filter(email=email).exists():
                result = {'result': 2, 'message': '邮箱未注册!'}
            else:
                user = User.objects.get(email=email)
                if user.password != password and not check_password(password, user.password):
                    result = {'result': 2, 'message': '密码不正确!'}
                else:
                    request.session['email'] = email
                    result = {'result': 0, 'message': '登录成功!', 'username': user.username,'avatar':user.avatar}
                    token = get_token(email)
                    result['token'] = token
                    request.session['token'] = token
                    result['userID'] = user.userID
        return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '前端炸了'}
        return JsonResponse(result)


@csrf_exempt
def email_register(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        email = data_json.get('email')
        if email.count('@') == 1:
            send_result = send_code_email(email)
            if not send_result:
                result = {'result': 2, 'message': '发送失败!请检查邮箱格式'}
                return JsonResponse(result)
            else:
                result = {'result': 0, 'message': '发送成功!请及时在邮箱中查收.'}
                return JsonResponse(result)
        else:
            result = {'result': 2, 'message': '邮箱格式不正确!'}
            return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def email_forget(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        email = data_json.get('email')
        if email.count('@') == 1:
            send_result = send_password_code_email(email)
            if not send_result:
                result = {'result': 2, 'message': '发送失败!请检查邮箱格式'}
                return JsonResponse(result)
            else:
                result = {'result': 0, 'message': '发送成功!请及时在邮箱中查收.'}
                return JsonResponse(result)
        else:
            result = {'result': 2, 'message': '邮箱格式不正确!'}
            return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def password_forget(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        email = data_json.get('email', 'null')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            code = data_json.get('code')
            if not EmailCode.objects.filter(code=code).exists():
                result = {'result': 2, 'message': '验证码错误!'}
                return JsonResponse(result)
            email_code = EmailCode.objects.get(code=code)
            now = datetime.datetime.now(timezone.utc)
            if (now - email_code.time).seconds > 300:
                return JsonResponse({'result': 2, 'message': "验证码已失效!"})
            email_code.delete()
            password = data_json.get('password')
            user.password = password
            user.save()
            result = {'result': 0, 'message': '修改成功!'}
            return JsonResponse(result)
        else:
            result = {'result': 2, 'message': '不存在该用户!'}
            return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def password_change(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        token = request.META.get('HTTP_AUTHORIZATION', 0)
        userID = check_token(token)
        if userID == -1:
            result = {'result': 10, 'message': 'Token有误!'}
            return JsonResponse(result)
        password = data_json.get('password')
        n_password = data_json.get('newPassword')
        user = User.objects.get(userID=userID)
        if user.password == password:
            user.password = n_password
            user.save()
            result = {'result': 0, 'message': '修改成功!'}
            return JsonResponse(result)
        else:
            result = {'result': 2, 'message': '密码不正确!'}
            return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def update(request):  # 修改用户基础信息
    if request.method == 'POST':
        data_json = json.loads(request.body)
        token = request.META.get('HTTP_AUTHORIZATION', 0)
        userID = check_token(token)
        if userID == -1:
            result = {'result': 10, 'message': 'Token有误!'}
            return JsonResponse(result)
        user = User.objects.get(userID=userID)
        user.sex = int(data_json.get('sex'))
        user.phone = data_json.get('phone')
        user.username = data_json.get('username')
        user.nickname = data_json.get('nickname')
        email = data_json.get('email')
        user.summary = data_json.get('summary')
        user.avatar = data_json.get('avatar')
        if email == user.email:
            user.email = data_json.get('email')
            user.save()
            result = {'result': 0, 'message': '修改成功!'}
            return JsonResponse(result)
        if User.objects.filter(email=email).exists():
            result = {'result': 2, 'message': '邮箱已注册!'}
            return JsonResponse(result)
        else:
            user.email = data_json.get('email')
            user.save()
            result = {'result': 0, 'message': '修改成功!'}
            return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def get_user(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION', 0)
        userID = check_token(token)
        if userID == -1:
            result = {'result': 10, 'message': 'Token有误!'}
            return JsonResponse(result)
        data_json = json.loads(request.body)
        userID = int(data_json.get('userID'))
        user = User.objects.get(userID=userID)
        data = {'username': user.username, 'nickname': user.nickname,
                'userID': user.userID, 'avatar': user.avatar, 'email': user.email, 'phone': user.phone,
                'summary': user.summary, 'sex': user.sex, }
        result = {'result': 0, 'message': '查询成功!', 'data': data}
        return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        source = request.FILES.get('file')
        if source:
            img = Img(img=source)
            img.save()
            result = {'result': 0, 'message': '上传成功!', 'url': 'http://43.138.77.8:8000' + img.img.url}
            return JsonResponse(result)
        else:
            result = {'result': 2, 'message': '请检查上传内容!'}
            return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def search(request):
    params = get_params(request, 'nameOrEmail')
    lack, lack_list = lack_check(params)
    if lack:
        return lack_error_res(lack_list)
    user_list = User.objects.all()
    count = 0
    result = []
    for user in user_list:
        if count == 10:
            break
        if user.email.find(params['nameOrEmail']) != -1 or user.username.find(params['nameOrEmail']) != -1:
            print(user.email.find(params['nameOrEmail']))
            result.append(user_simple_info(user))
            count += 1
    return good_res('完成用户搜索', content={'userList': result})


@csrf_exempt
def update_ava(request):
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'avatar')
    vals['userID'] = userID
    lack, lack_list = lack_check(vals)
    if lack:
        return lack_error_res(lack_list)
    user = User.objects.get(userID=userID)
    if vals['avatar']:
        user.avatar = vals['avatar']
        user.save()
        result = {'result': 0, 'message': '上传成功!'}
        return JsonResponse(result)
    else:
        result = {'result': 2, 'message': '请检查上传内容!'}
        return JsonResponse(result)

@csrf_exempt
def get_avatar(request):
    if request.method != 'POST':
        return method_err_res()
    data_json = json.loads(request.body)
    userID = int(data_json.get('userID'))
    user = User.objects.get(userID=userID)
    result = {'result': 0, 'message': '获取成功','username':user.username,'avatar':user.avatar}
    return JsonResponse(result)
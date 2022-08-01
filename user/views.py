import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict, JsonResponse
from backend.utils.utils import *
from .models import *
from datetime import timedelta
from backend.backend import settings
from datetime import date, timezone


@csrf_exempt
def put(request):
    if request.method == 'PUT':
        a = QueryDict(request.body)
        s = list(a.items())[0][0]
        print(s)
        print(type(s))
        data_json = json.loads(request.body)
        print(data_json)
        key = data_json['key']
        field = data_json['field']
        print(key, field)
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def delete(request):
    if request.method == 'DELETE':
        a = QueryDict(request.body)
        s = list(a.items())[0][0]
        print(s)
        print(type(s))
        data_json = json.loads(request.body)
        print(data_json)
        key = data_json['key']
        field = data_json['field']
        print(key, field)
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def get(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        field = request.GET.get('field')
        print(key, field)
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def post(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        field = request.POST.get('field')
        print(key, field)
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        username = data_json.get('username')
        password = data_json.get('password')
        email = data_json.get('email')
        nickname = data_json.get('nickname')
        code = data_json.get('code')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'result': 0, 'message': "邮箱已注册!"})
        else:
            if not EmailCode.objects.filter(code=code).exists():
                return JsonResponse({'result': 0, 'message': "验证码错误!"})
            email_code = EmailCode.objects.get(code=code)
            now = datetime.datetime.now(timezone.utc)
            if (now - email_code.time).seconds > 300:
                return JsonResponse({'result': 0, 'message': "验证码已失效!"})
            users = User.objects.all()
            count = len(users)
            new_user = User(userID=count, username=username, nickname=nickname, password=password, email=email)
            new_user.save()
        return JsonResponse({'result': 1, 'message': "注册成功!"})
    else:
        return JsonResponse({'result': 0, 'message': "前端炸了!"})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        email = data_json.get('email')
        password = data_json.get('password')
        if len(email) == 0 or len(password) == 0:
            result = {'result': 0, 'message': '邮箱与密码不允许为空!'}
        else:
            if not User.objects.filter(email=email).exists():
                result = {'result': 0, 'message': '邮箱未注册!'}
            else:
                user = User.objects.get(email=email)
                if user.password != password:
                    result = {'result': 0, 'message': '密码不正确!'}
                else:
                    request.session['email'] = email
                    result = {'result': 1, 'message': '登录成功!', 'username': user.username}
                    token = gettoken(email)
                    result['token'] = token
                    request.session['token'] = token
                    result['userID'] = user.userID
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '前端炸了'}
        return JsonResponse(result)


@csrf_exempt
def email_register(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        email = data_json.get('email')
        if email.count('@') == 1:
            send_result = send_code_email(email)
            if not send_result:
                result = {'result': 0, 'message': '发送失败!请检查邮箱格式'}
                return JsonResponse(result)
            else:
                result = {'result': 1, 'message': '发送成功!请及时在邮箱中查收.'}
                return JsonResponse(result)
        else:
            result = {'result': 0, 'message': '邮箱格式不正确!'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def email_forget(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        email = data_json.get('email')
        if email.count('@') == 1:
            send_result = send_password_code_email(email)
            if not send_result:
                result = {'result': 0, 'message': '发送失败!请检查邮箱格式'}
                return JsonResponse(result)
            else:
                result = {'result': 1, 'message': '发送成功!请及时在邮箱中查收.'}
                return JsonResponse(result)
        else:
            result = {'result': 0, 'message': '邮箱格式不正确!'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '前端炸了!'}
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
                result = {'result': 0, 'message': '验证码错误!'}
                return JsonResponse(result)
            email_code = EmailCode.objects.get(code=code)
            now = datetime.datetime.now(timezone.utc)
            if (now - email_code.time).seconds > 300:
                return JsonResponse({'result': 0, 'message': "验证码已失效!"})
            email_code.delete()
            password = data_json.get('password')
            user.password = password
            user.save()
            result = {'result': 1, 'message': '修改成功!'}
            return JsonResponse(result)
        else:
            result = {'result': 0, 'message': '不存在该用户!'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def password_change(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        token = request.META.get('HTTP_AUTHORIZATION', 0)
        userID = check(token)
        if userID == -1:
            result = {'result': 0, 'message': 'Token有误!'}
            return JsonResponse(result)
        password = data_json.get('password')
        n_password = data_json.get('n_password')
        user = User.objects.get(userID=userID)
        if user.password == password:
            user.password = n_password
            user.save()
            result = {'result': 1, 'message': '修改成功!'}
            return JsonResponse(result)
        else:
            result = {'result': 0, 'message': '密码不正确!'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def upload_info(request):  # 修改用户基础信息
    if request.method == 'POST':
        data_json = json.loads(request.body)
        token = request.META.get('HTTP_AUTHORIZATION', 0)
        userID = check(token)
        if userID == -1:
            result = {'result': 0, 'message': 'Token有误!'}
            return JsonResponse(result)
        user = User.objects.get(userID=userID)
        user.sex = int(data_json.get('sex'))
        user.phone = data_json.get('phone')
        user.username = data_json.get('username')
        user.nickname = data_json.get('nickname')
        email = data_json.get('email')
        user.summary = data_json.get('summary')
        if email == user.email:
            user.email = data_json.get('email')
            user.save()
            result = {'result': 1, 'message': '修改成功!'}
            return JsonResponse(result)
        if User.objects.filter(email=email).exists():
            result = {'result': 0, 'message': '邮箱已注册!'}
            return JsonResponse(result)
        else:
            user.email = data_json.get('email')
            user.save()
            result = {'result': 1, 'message': '修改成功!'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def upload_avatars(request):  # 修改头像
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION', 0)
        userID = check(token)
        if userID == -1:
            result = {'result': 0, 'message': 'Token有误!'}
            return JsonResponse(result)
        source = request.FILES.get('file')
        if source:
            if User.objects.filter(userID=userID).exists():
                user = User.objects.get(userID=userID)
                user.header = source
                user.save()
                result = {'result': 1, 'userID': userID, 'url': user.get_photo_url}
            else:
                result = {'result': 0, 'message': '未找到该用户!'}
            return JsonResponse(result)
        else:
            result = {'result': 0, 'message': '请检查上传内容!'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def get_user(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION', 0)
        userID = check(token)
        if userID == -1:
            result = {'result': 0, 'message': 'Token有误!'}
            return JsonResponse(result)
        user = User.objects.get(userID=userID)
        result = {'result': 1, 'message': '查询成功!', 'username': user.username, 'nickname': user.nickname,
                  'userID': userID, 'url': user.get_photo_url, 'email': user.email, 'phone': user.phone,
                  'summary': user.summary, 'sex': user.sex,
                  }
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)

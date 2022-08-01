from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse
from jwt import encode
from jwt import decode
import datetime
from backend.user.models import *
from random import Random
from django.core.mail import send_mail  # 发送邮件模块
from backend.backend import settings  # setting.py添加的的配置信息
import datetime
import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse, HttpRequest

from jwt import encode
from jwt import decode
import datetime
from backend.user.models import *


# from user.models import User


# ----------------- 实用小工具 ----------------------

# 检查是否已登录
def login_check(request):
    return 'userID' in request.session


# 能少写几个字母
def res(errno, message):
    return JsonResponse({'errno': errno, "msg": message})


# 一次性get所有参数, args为可变参数列表
def get_params(request, *args):
    assert isinstance(request, HttpRequest)
    data_json = json.loads(request.body)
    result = {}
    for arg in args:
        result[str(arg)] = result[str(arg)]
    return result


# 检查一个字典中是否有none
def check_lack(obj_dic):
    lack_list = []
    for key, obj in obj_dic.items():
        if obj is None:
            lack_list.append(key)
    if len(lack_list) > 0:
        return True, lack_list
    return False, None


def simple_res(code, message):
    return JsonResponse({'result': code, 'message': message})


# # 从用户名或邮箱获取用户对象
# def get_user(username_or_email):
#     username_or_email = str(username_or_email)
#     user = None
#     try:
#         user = User.objects.get(username=username_or_email)
#     except ObjectDoesNotExist:
#         pass
#         # return False, res(3005, "不存在 "+username+" 这个用户")
#     except MultipleObjectsReturned:
#         return False, res(1, "有多个用户具有名称 "+username_or_email+" ，这是一个bug")
#     if user is not None:
#         return True, user
#     try:
#         user = User.objects.get(email=username_or_email)
#     except ObjectDoesNotExist:
#         return False, res(3005, username_or_email+" 不是任何用户的用户名或邮箱")
#     except MultipleObjectsReturned:
#         return False, res(1, "有多个用户具有邮箱 "+username_or_email+" ，这是一个bug")
#     return True, user


# ------------------ 通用异常 -----------------------

# 未甄别的错误，直接返回异常信息
# def unknown_err(exception):
#     return res(1, repr(exception))
# 后来想了想，不如不处理这种异常，直接在前端看见完整的异常信息

def method_err():
    return res(2, '请求方式错误')


def need_login():
    return res(3, '此操作需要登录')


# 传过来的数据存在缺项
def lack_err(lack_list):
    return JsonResponse({
        'errno': 4,
        'msg': '请求缺少字段',
        'lack_list': list(lack_list),
    })


# ------------------ token模块 -----------------------


def get_token(email):
    time = datetime.datetime.now()
    return encode({'email': email, 'login_time': str(time), 'id': User.objects.get(email=email).userID
                   }, 'secret_key', algorithm='HS256')


def check_token(token):
    try:
        s = decode(token, 'secret_key', algorithms=['HS256'])
    except:
        return -1
    return s.get('id', -1)


# ------------------ email模块 -----------------------
# 生成随机字符串
def random_str(randomlength=8):
    s = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        s += chars[random.randint(0, length)]
    return s


def send_code_email(email):
    code = random_str(6)
    newcode = EmailCode()
    newcode.code = code
    newcode.save()
    email_title = "墨书软件项目管理系统注册激活验证码"
    email_body = "欢迎您注册墨书软件项目管理系统!\n"
    email_body += "您的邮箱注册验证码为：{0}, 该验证码有效时间为五分钟，请及时进行验证.\n".format(code)
    email_body += "如果您从未注册过墨书软件项目管理系统,请忽略该邮件."
    send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
    return send_status


def send_password_code_email(email):
    code = random_str(6)
    newcode = EmailCode()
    newcode.code = code
    newcode.save()
    email_title = "墨书软件项目管理系统密码重置验证码"
    email_body = "您的密码重置验证码为：{0}, 该验证码有效时间为五分钟，请及时修改密码.\n".format(code)
    email_body += "如果您从未注册过墨书软件项目管理系统,请忽略该邮件."
    send_status = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
    return send_status


def check_code(code):
    if not EmailCode.objects.filter(code=code).exists():
        return False
    else:
        EmailCode.objects.filter(code=code).delete()
        return True

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse
from jwt import encode
from jwt import decode
import datetime
from user.models import *
from random import Random
from django.core.mail import send_mail  # 发送邮件模块
from backend import settings  # setting.py添加的的配置信息
import datetime
import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse, HttpRequest

from jwt import encode
from jwt import decode
import datetime
from user.models import *


# from user.models import User






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

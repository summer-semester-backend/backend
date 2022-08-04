# 各种同类函数不<3个的函数
# 如果同类函数>=3个, 应另开一个文件

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
from team.models import Team, Team_User


# from user.models import User



def user_simple_info(user):
    return {'userID':user.userID, 'username':user.username, 'email':user.email}


# def team_simple_info(team):
#     return {
#         'teamID': team.teamID,
#         'teamName': team.team_name,
#         'teamCreateTime': team.create_time,
#     }


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


def get_user_id(request):
    token = request.META.get('HTTP_AUTHORIZATION', 0)
    userID = check_token(token)
    if userID == -1:
        result = {'result': 0, 'message': 'Token有误!'}
        return False, JsonResponse(result)
    return True, userID

def get_user(request):
    success, id = get_user_id(request)
    if not success:
        return None
    try:
        user = User.objects.get(userID=id)
    except:
        return None
    return user




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


def get_user_auth(user, team):
    assert isinstance(user, User)
    assert isinstance(team, Team)
    tu = Team_User.objects.filter(user=user, team=team)
    # auth = tu.authority
    if len(tu) == 0:  # 用户不在此团队
        return -100
    if len(tu) == 1:
        return tu[0].authority
    raise Exception('有多个权限信息')
    # return -2  # 有多个权限信息

def set_user_auth(user, team, auth):
    assert isinstance(user, User)
    assert isinstance(team, Team)
    tu = Team_User.objects.filter(user=user, team=team)
    # auth = tu.authority
    if len(tu) == 0:  # 用户不在此团队
        return
    if len(tu) == 1:
        return tu[0].authority
    raise Exception('有多个权限信息')
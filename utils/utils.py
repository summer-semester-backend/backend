import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse, HttpRequest

from jwt import encode
from jwt import decode
import datetime
from user.models import *

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





def get_token(email):
    time = datetime.datetime.now()
    return encode({'email': email, 'login_time': str(time), 'id': UserInfo.objects.get(email=email).userID
                   }, 'secret_key', algorithm='HS256')


def check_token(token):
    try:
        s = decode(token, 'secret_key', algorithms=['HS256'])
    except:
        return -1
    return s.get('id', -1)

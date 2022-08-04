from .models import File, FType
from team.models import Team
from user.tools import *
from utils.utils import *
from utils.responce import *
from utils.params import *
from team.models import *

def file_general_check(request, method, params, authority=-100):
    """文件操作的各种检查
    如果有问题, 则返回内容为
    {
        'success': False
        'res': 一个准备好的JsonResponse, 可以直接返回给前端
    }
    如果检查无误则返回内容为
    {
        'success': True
        'user': 本用户
        'file': 要操作的文件
        'vals': {} (所有参数)
    }

    参数:
    - request 传入的请求
    - method 希望的请求方法
    - params 需要那些参数
    - authority 本操作需要的权限. 不填的情况下意味着任何用户都可以执行.

    检查事项:
    - 请求方法正确
    - 已登录
    - 参数齐全
    - fileID对应的文件存在
    - 权限足够
        - 如果是团队文件则需要本用户权限≥authority
        - 如果是个人文件则需要是creator
    """
    result = {'success': False}
    # 登录检查
    user = get_user(request)
    if user is None:
        result['res'] = not_login_res()
        return result
    # 获取参数
    vals = get_params_by_list(request, params)
    lack, lack_list = lack_check(vals)
    if lack:
        result['res'] = lack_error_res(lack_list)
        return result
    file = id_to_file(vals['fileID'])
    if file is None:
        result['res'] = error_res('找不到文件')
        return result
    # 权限检查
    if file.team is not None:
        team = file.team
        auth = get_user_auth(user, team)
        if auth < authority:
            result['res'] = bad_authority_res('文件操作')
            return result
    else:
        if file.file_creator.userID != user.userID:
            return error_res('不能访问别人的个人文件')
    result['success'] = True
    return result | {
        'user': user,
        'file': file,
        'vals': vals,
    }


def id_to_file(fileID, team=None, user=None):
    if fileID == -1:
        if team is not None:
            return team.root_file  # 优先查团队根文件
        elif user is not None:
            raise Exception('用户根目录尚未实现')
        else:
            raise Exception('fileID是-1的话, team和user至少给出一个')
    try:
        file = File.objects.get(fileID=fileID)
    except:
        return None
    return file

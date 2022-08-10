from .models import File, FType, Share
from team.models import Team
from user.tools import *
from utils.utils import *
from utils.responce import *
from utils.params import *
from team.models import *


def get_share_auth(share_code, file):
    share_list = Share.objects.filter(file=file, share_code=share_code)
    if len(share_list) == 0:
        return C.forbidden
    for share in share_list:
        if (datetime.datetime.now() - share.create_time.replace(tzinfo=None)).seconds <= 604800:
            return C.readonly
        else:
            share.delete()
    return C.forbidden


def file_general_check(request, method, params, authority=C.forbidden, optional_params=None):
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
    if optional_params is None:
        optional_params = []
    result = {'success': False}
    # 获取参数
    vals = get_params_by_list(request, params, optional_arg_list=optional_params)
    lack, lack_list = lack_check(vals)
    if lack:
        result['res'] = lack_error_res(lack_list)
        return result
    if vals['fileID'] != -1:
        file = id_to_file(vals['fileID'])
    else:
        if 'teamID' not in vals:
            result['res'] = error_res('fileID为-1的时候需要给出teamID')
            return result
        team_list = Team.objects.filter(teamID=vals['teamID'])
        if not team_list.exists():
            result['res'] = error_res('团队不存在')
            return result
        team = Team.objects.get(teamID=vals['teamID'])
        file = id_to_file(vals['fileID'], team=team)
    if file is None:
        result['res'] = error_res('找不到文件')
        return result
    team = None
    # 权限检查1 (分享产生的权限)
    auth = -100
    if 'shareCode' in vals:
        auth = max(auth, get_share_auth(share_code=vals['shareCode'], file=file)) # 获取文件分享权限(如果存在的话)
    # 登录检查
    user = get_user(request)
    result.update({
        'user': user,
        'file': file,
        'vals': vals,
    })
    if user is None: # 未登录, 通常来说是错误
        if auth == C.forbidden:
            result['res'] = not_login_res()
            return result
        elif auth >= authority: # 是通过分享链接打开的? 提前返回
            result['success'] = True
            return result
    # 权限检查2 (团队身份产生的权限)
    if file.team is not None:
        team = file.team
        auth = max(auth, get_user_auth(user, team))
        if auth < authority:
            result['res'] = resource_not_found_res()
            return result
    else:
        if file.file_creator.userID != user.userID:
            result['res'] = error_res('不能访问别人的个人文件')
            return result
    result['success'] = True
    return result


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


def inherit(file, father):
    """从father处继承必要的信息"""


def copy_implement(file, father, level=0):
    """
    复制文件和其下属的内容到指定的父文件下方, 新文件的所有权和father保持一致
    - file: 被复制的文件
    - father: 要复制到的位置
    """
    if level == 20:
        raise Exception('递归层数达到20, 疑似无限递归')
    print("level = {}".format(level))
    assert isinstance(file, File)
    assert isinstance(father, File)
    if not father.is_dir():
        raise Exception(father.file_name+"不是文件夹, 无法作为父目录")
    # 提前获取下属文件列表, 避免无限递归
    son_list = []
    if file.is_dir():
        son_list = File.objects.filter(father=file)
    print(len(son_list))
    # print(son_list[0].fileID)
    # 创建file的副本
    copy = file.copy()
    assert isinstance(copy, File)
    # 从father继承必要的信息
    copy.team = father.team
    copy.save()
    # 如果是同目录下复制, 在文件名后面添加'-副本'
    for son in son_list:
        # print(son.file_name)
        if not son.is_deleted:
            copy_implement(son, copy, level+1)
    copy.father = father
    if copy.father.fileID == file.father.fileID:
        copy.file_name += ' - 副本'
    copy.save()
    return copy


def name_duplicate_killer(file):
    """
    检测并消灭重名问题, 如果改名则返回True, 没重名返回False
    """
    print(type(file))
    assert isinstance(file, File)
    if file.father is None:
        return False
    file_list = File.objects.filter(father=file.father,type=file.type)

    name_set = set()
    for f in file_list:
        if f.fileID != file.fileID:
            name_set.add(f.file_name)
            # file_list.remove(f)
            # break
    # name_set = set([f.file_name for f in file_list])
    changed = False
    while file.file_name in name_set:
        file.file_name += '*'
        changed = True
    return changed

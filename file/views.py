from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from utils.responce import res, good_res, warning_res, error_res
from utils.responce import method_err_res, not_login_res, bad_authority_res
from utils.params import lack_error_res, lack_check, get_params, get_params_by_list
from utils.utils import get_user_id, get_user, get_user_auth, random_str, user_simple_info

from .models import File, FType
from team.models import Team, C

from .tools import id_to_file, file_general_check
from team.tools import id_to_team
from user.tools import id_to_user


@csrf_exempt
def create(request):
    # 登录检查
    user = get_user(request)
    if user is None:
        return not_login_res()
    # 获取参数
    params = get_params_by_list(
        request,
        ['fileName', 'fileType', 'fileImage', 'fatherID'],
        ['teamID'],
    )
    lack, lack_list = lack_check(params)
    if lack:
        return lack_error_res(lack_list)
    # 检查父文件存在性
    team = None
    if 'teamID' in params:
        team = id_to_team(params['teamID'])
    # user = id_to_user(params['userID'])
    father = id_to_file(params['fatherID'], team, user)
    if father is None:
        return error_res('找不到父文件')
    file = File.objects.create(
        file_name=params['fileName'],
        type=params['fileType'],
        fileImage=params['fileImage'],
        father=father,
        file_creator=user,
    )
    if team is not None:
        file.team = team
    file.save()
    return good_res('成功创建文件')


@csrf_exempt
def read(request):
    check = file_general_check(request, 'POST', ['fileID'], C.member)
    if not check['success']:
        return check['res']
    file = check['file']
    assert isinstance(file, File)
    info = file.info()
    content = file.content()
    if file.is_dir():
        result = {'sonList': content}
    else:
        result = {'data': content}
    return good_res('成功读取文件', info | result)


@csrf_exempt
def write(request):
    check = file_general_check(request, 'POST', ['fileID'], C.member)
    if not check['success']:
        return check['res']
    file = check['file']
    assert isinstance(file, File)
    vals = get_params_by_list(
        request,
        arg_list=[],
        optional_arg_list=['fileName', 'fileImage', 'fatherID', 'data']
    )
    if 'fileName' in vals:
        file.file_name = vals['fileName']
    if 'fileImage' in vals:
        file.file_image = vals['fileImage']
    if 'fatherID' in vals:
        father = id_to_file(vals['fatherID'], file.team, file.file_creator)
        if father is None:
            return error_res('找不到父文件')
        file.father = father
    if 'data' in vals:
        file.data = vals['data']
    file.save()
    return good_res('文件修改已保存')

from django.views.decorators.csrf import csrf_exempt

from utils.responce import res, good_res, warning_res, error_res
from utils.responce import method_err_res, not_login_res, bad_authority_res
from utils.params import lack_error_res, lack_check, get_params, get_params_by_list
from utils.utils import get_user_id, get_user, get_user_auth, random_str, user_simple_info
import json
from .models import File, FType, Share,Image

from .tools import id_to_file, file_general_check, copy_implement, name_duplicate_killer
from team.tools import id_to_team

import datetime
from jwt import encode
from user.models import User
from team.models import Team, Team_User, C
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FType, File
from utils.responce import res, good_res, warning_res, error_res
from utils.responce import method_err_res, not_login_res, bad_authority_res
from utils.params import lack_error_res, lack_check, get_params
from utils.utils import *


@csrf_exempt
def create(request):
    """
    创建文件时, 如果给出不是-1的fatherID, 就无视teamID
    如果fatherID是-1, 就认为
    """
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
    # print(params)
    lack, lack_list = lack_check(params)
    if lack:
        return lack_error_res(lack_list)
    # 检查父文件存在性
    team = None
    if 'teamID' in params:
        team = id_to_team(params['teamID'])
    # print(team.info())
    # user = id_to_user(params['userID'])
    father = id_to_file(params['fatherID'], team, user)
    if father is None:
        return error_res('找不到父文件')
    team = father.team
    # 检查文件类型合法性
    params['fileType'] = int(params['fileType'])
    if params['fileType'] not in FType.available_list:
        return error_res(str(params['fileType']) + '不是任何类型')
    if params['fileImage'] == "" and params['fileType'] == 1:
        params['fileImage'] = "http://43.138.77.8:8000/media/image/20220805/20220805220731_38.png"
    # 解决重名问题
    # tmp = File.objects.filter(father=father, file_name=params['fileName'], is_deleted=0)
    # warning = False
    # while tmp.exists():
    #     params['fileName'] += '*'
    #     warning = True
    #     tmp = File.objects.filter(father=father, file_name=params['fileName'], is_deleted=0)
    file = File.objects.create(
        file_name=params['fileName'],
        type=params['fileType'],
        file_image=params['fileImage'],
        father=father,
        file_creator=user,
    )
    warning = name_duplicate_killer(file)
    if team is not None:
        file.team = team
    file.save()
    if warning:
        return warning_res('同路径下不可重名, 已自动在项目/文件名后增加*号')
    return good_res('成功创建文件')


@csrf_exempt
def read(request):
    check = file_general_check(
        request,
        'POST',
        ['fileID'],
        C.readonly,
        optional_params=['teamID', 'shareCode']
    )
    if not check['success']:
        return check['res']
    if check['user'] is None:
        print("not login but success")
    file = check['file']
    assert isinstance(file, File)
    info = file.info()
    content = file.content()
    if file.is_dir():
        result = {'sonList': content}
    else:
        result = content
    file.last_visit_time = datetime.datetime.now()
    file.save()
    info.update(result)
    return good_res('成功读取文件', info)


@csrf_exempt
def write(request):
    check = file_general_check(request, 'POST', ['fileID'], C.member)
    if not check['success']:
        return check['res']
    file = check['file']
    assert isinstance(file, File)
    vals = get_params_by_list(
        request,
        arg_list=['fileID'],
        optional_arg_list=['fileName', 'fileImage', 'fatherID', 'data','previewImages']
    )
    if 'fatherID' in vals:
        father = id_to_file(vals['fatherID'], file.team, file.file_creator)
        if father is None:
            return error_res('找不到父文件')
        if not father.is_dir():
            return error_res('父文件必须是文件夹')
        file.father = father
    # 检查文件名, 如果和相同father下面有重复, 就给加上后缀*, 并返回warning
    tmp = File.objects.get(fileID=vals['fileID'])
    if 'previewImages' in vals:
        image_list=Image.objects.filter(fileID=vals['fileID'])
        if image_list.exists:
            for image in image_list:
                image.delete()
            for protoType in vals['previewImages']:
                Image.objects.create(fileID=vals['fileID'],preview_image=protoType)
        else:
            for protoType in vals['previewImages']:
                Image.objects.create(fileID=vals['fileID'],preview_image=protoType)
    warning = False
    if 'fileName' in vals:
        if tmp.file_name != vals['fileName']:
            tmp = File.objects.filter(father=file.father, file_name=vals['fileName'], is_deleted=0)
            while tmp.exists():
                vals['fileName'] += '*'
                warning = True
                tmp = File.objects.filter(father=file.father, file_name=vals['fileName'], is_deleted=0)
            if 'fileName' in vals:
                file.file_name = vals['fileName']
            if 'fileImage' in vals:
                file.file_image = vals['fileImage']
            if 'data' in vals:
                file.data = vals['data']
            file.save()
        else:
            if 'fileImage' in vals:
                file.file_image = vals['fileImage']
            if 'data' in vals:
                file.data = vals['data']
            file.save()
        if warning:
            return warning_res('修改已保存, 但同路径下不可重名, 已自动在项目/文件名后增加*号')
        return good_res('修改已保存')
    else:
        if 'fileImage' in vals:
            file.file_image = vals['fileImage']
        if 'data' in vals:
            file.data = vals['data']
        file.save()
        return good_res('修改已保存')


@csrf_exempt
def delete_file(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    vals = get_params(request, 'fileID')
    vals['userID'] = userID
    lack, lack_list = lack_check(vals)
    if lack:
        return lack_error_res(lack_list)
    file_list = File.objects.filter(fileID=vals['fileID'])
    if len(file_list) == 0:
        return error_res('文件不存在')
    file = File.objects.get(fileID=vals['fileID'])
    if file.is_deleted == 1:
        file.delete()
    else:
        file.is_deleted = 1
        file.abandon_time = datetime.datetime.now()
        file.save()
    return res(0, '文件删除成功')


@csrf_exempt
def recover_file(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    vals = get_params(request, 'fileID')
    vals['userID'] = userID
    lack, lack_list = lack_check(vals)
    if lack:
        return lack_error_res(lack_list)
    file_list = File.objects.filter(fileID=vals['fileID'])
    if len(file_list) == 0:
        return error_res('文件不存在')
    file = File.objects.get(fileID=vals['fileID'])
    if file.is_deleted == 0:
        return res(2, '文件不存在')
    else:
        tmp = File.objects.filter(father=file.father, file_name=file.file_name, is_deleted=0)
        if tmp.exists():
            name = file.file_name
            while tmp.exists():
                name += '*'
                warning = True
                tmp = File.objects.filter(father=file.father, file_name=name, is_deleted=0)
            file.file_name = name
            file.is_deleted = 0
            file.save()
            return warning_res('文件已恢复, 但同路径下不可重名, 已自动在项目/文件名后增加*号')
        else:
            file.is_deleted = 0
            file.save()
            return res(0, '文件恢复成功')


@csrf_exempt
def project_last_visit(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    user = User.objects.get(userID=userID)
    team_list = Team_User.objects.filter(user=user)
    project_list = []
    for team in team_list:
        if get_user_auth(user, team.team) >= 0:
            project_list += File.objects.filter(team=team.team, type=1, is_deleted=0).order_by('-last_visit_time')
    result_list = []
    ss = []
    for project in project_list:
        if get_user_auth(user, project.team) >= 0:
            s = project.last_visit_time.strftime('%Y-%m-%d %H:%M:%S')
            content = {'fileID': project.fileID, 'fileName': project.file_name,
                       'fileImage': project.file_image, 'createTime': project.create_time,
                       'lastVisitTime': project.last_visit_time, 'teamName': project.team.team_name,
                       'userName': project.file_creator.username, 's': s}
            ss.append(content)
    ss.sort(key=lambda s: s["s"], reverse=True)
    for project in ss[:6]:
        result_list.append(project)
    content = {'list': result_list}
    return res(0, '查询成功', content)


@csrf_exempt
def clear_bin(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    data_json = json.loads(request.body)
    fileID = int(data_json['fileID'])
    if fileID == -1:
        teamID = int(data_json['teamID'])
        team = Team.objects.get(teamID=teamID)
        file_list = File.objects.filter(team=team, is_deleted=1)
        result_list = []
        for file in file_list:
            file.delete()
        return res(0, '清空成功')
    else:
        rubbish_list=[]
        file=File.objects.get(fileID=fileID)
        find_rubbish(file,rubbish_list)     
        result_list = []
        for rubbish in rubbish_list:
            rubbish.delete()
        return res(0, '清空成功')


@csrf_exempt
def bin_list(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    data_json = json.loads(request.body)
    fileID = int(data_json['fileID'])
    if fileID == -1:
        teamID = int(data_json['teamID'])
        team = Team.objects.get(teamID=teamID)
        file_list = File.objects.filter(team=team, is_deleted=1)
        result_list = []
        for file in file_list:
            content = {'fileID': file.fileID, 'fileName': file.file_name,
                       'abandonTime': file.abandon_time, 'fileType': file.type,'userName':file.file_creator.username}
            result_list.append(content)
        content = {'list': result_list}
        return res(0, '查询成功', content)
    else:
        rubbish_list=[]
        file=File.objects.get(fileID=fileID)
        find_rubbish(file,rubbish_list)
        
        result_list = []
        for rubbish in rubbish_list:
            content = {'fileID': rubbish.fileID, 'fileName': rubbish.file_name,
                        'abandonTime': rubbish.abandon_time, 'teamName': rubbish.team.team_name,
                        'fileType': rubbish.type,'userName':rubbish.file_creator.username}
            result_list.append(content)
        content = {'list': result_list}
        return res(0, '查询成功', content)


@csrf_exempt
def all(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    user = User.objects.get(userID=userID)
    team_list = Team_User.objects.filter(user=user)
    project_list = []
    for team in team_list:
        if get_user_auth(user, team.team) >= 0:
            project_list += File.objects.filter(team=team.team, type=1, is_deleted=0)
    result_list = []
    ss = []
    for project in project_list:
        if get_user_auth(user, project.team) >= 0:
            s = project.create_time.strftime('%Y-%m-%d %H:%M:%S')
            content = {'fileID': project.fileID, 'fileName': project.file_name,
                       'fileImage': project.file_image, 'createTime': project.create_time,
                       'lastVisitTime': project.last_visit_time, 'teamName': project.team.team_name,
                       'userName': project.file_creator.username, 's': s}
            ss.append(content)
    ss.sort(key=lambda s: s["s"], reverse=True)
    for project in ss:
        result_list.append(project)
    content = {'list': result_list}
    return res(0, '查询成功', content)


@csrf_exempt
def center_read(request):
    check = file_general_check(
        request,
        'POST',
        ['fileID'],
        C.member,
        optional_params=['teamID']
    )
    if not check['success']:
        return check['res']
    file = check['file']
    assert isinstance(file, File)
    info = file.info()
    if 'teamID' in check['vals']:
        content = file.center(True)
    else:
        content = file.center(False)
    if file.is_dir():
        result = {'sonList': content}
    else:
        result = content
    file.last_visit_time = datetime.datetime.now()
    file.save()
    info.update(result)
    return good_res('成功读取文件', info)

@csrf_exempt
def copy(request):
    check = file_general_check(
        request,
        'POST',
        ['fileID', 'fatherID'],
        C.member,
        ['teamID', 'newName'],
    )
    if not check['success']:
        return check['res']
    file = check['file']
    assert isinstance(file, File)
    fatherID = check['vals']['fatherID']
    user = get_user(request)
    team = None
    if 'teamID' in check['vals']:
        team = id_to_team(check['vals']['teamID'])
    # 获取father
    if fatherID == -1 and team is None:
        father = file.father
    else:
        father = id_to_file(fatherID, team, user)
    if father is None:
        return error_res('父文件不存在')
    team = father.team
    #操作合法性检查
    # if (file.team is None) != (father.team is None):
    #     if file.team is None:
    #         return error_res('个人文件只能复制为个人文件')
    #     else:
    #         return error_res('团队文件只能复制为团队文件')
    # if team is not None and father.team.teamID is not file.team.teamID:
    #     return error_res('父文件需要属于同一团队')
    # if team is None and father.file_creator.userID is not file.file_creator.userID:
    #     return error_res('父文件不是你自己的文件')
    # 实施复制
    copy_instance = copy_implement(file, father)
    if copy_instance.type==15:
        copy_instance.type=14
        copy_instance.save()
    if 'newName' in check['vals']:
        copy_instance.file_name = check['vals']['newName']
    copy_instance.file_creator=user
    copy_instance.save()
    if copy_instance.type==13:
        image_list=Image.objects.filter(fileID=file.fileID)
        for image in image_list:
            Image.objects.create(fileID=copy_instance.fileID,preview_image=image.preview_image)
    if name_duplicate_killer(copy_instance):
        copy_instance.save()
        return warning_res('复制完成, 但由于文件重名, 已自动增加后缀*号')
    return good_res('复制完成')


def find_rubbish(file,rubbish_list:list):
    file_list=File.objects.filter(father=file)
    if file_list.exists():
        for file in file_list:
            if file.is_deleted==1:
                rubbish_list.append(file)
            else:
                find_rubbish(file,rubbish_list)
    else:
        return

@csrf_exempt
def common_template_text_read(request):
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    data_json = json.loads(request.body)
    fileID = int(data_json['fileID'])
    if fileID == -1:
        file=File.objects.get(fileID=268)
        info = file.info()
        content = file.content()
        if file.is_dir():
            result = {'sonList': content}
        else:
            result = content
        file.last_visit_time = datetime.datetime.now()
        file.save()
        info.update(result)
        return good_res('成功读取文件', info)
    else:
        file=File.objects.get(fileID=fileID)
        info = file.info()
        content = file.content()
        if file.is_dir():
            result = {'sonList': content}
        else:
            result = content
        file.last_visit_time = datetime.datetime.now()
        file.save()
        info.update(result)
        return good_res('成功读取文件', info)

@csrf_exempt
def ancestor(request):
    check = file_general_check(
        request,
        'POST',
        ['fileID'],
        C.member,
    )
    if not check['success']:
        return check['res']
    file = check['file']
    assert isinstance(file, File)
    result_list=[]
    info = file.info()
    result_list.append(info)
    while file.father != None and file.father.type != 0:
        result_list.append(file.father.info())
        file=file.father
    result_list.reverse()
    info={'list':result_list}
    return good_res('成功读取祖先文件', info)

@csrf_exempt
def template_read(request):
    check = file_general_check(
        request,
        'POST',
        ['fileID','teamID'],
        C.member,
    )
    if not check['success']:
        return check['res']
    file = check['file']
    if check['vals']['fileID'] != -1:
        file=file.team.root_file
    assert isinstance(file, File)
    info = file.info()
    content = file.template()
    result = {'sonList': content}
    file.last_visit_time = datetime.datetime.now()
    file.save()
    info.update(result)
    return good_res('成功读取团队模板', info)


@csrf_exempt
def create_template(request):
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    data_json = json.loads(request.body)
    fileID = int(data_json['fileID'])
    fileName = data_json['fileName']
    data = data_json['data']
    file=File.objects.get(fileID=fileID)
    user=User.objects.get(userID=userID)
    file = File.objects.create(
        file_name=fileName,
        type=15,
        father=file.team.root_file,
        file_creator=user,
        team=file.team,
        data=data
    )
    warning = name_duplicate_killer(file)
    file.save()
    if warning:
        return warning_res('同路径下不可重名, 已自动在项目/文件名后增加*号')
    return good_res('成功创建团队模板')


@csrf_exempt
def share(request):
    check = file_general_check(
        request,
        'POST',
        ['fileID'],
        C.member,
    )
    if not check['success']:
        return check['res']
    file = check['file']
    share_code = random_str(10)
    Share.objects.create(file=file, share_code=share_code)
    return good_res('分享成功', {'shareCode':share_code})

    
@csrf_exempt
def common_read(request):
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    data_json = json.loads(request.body)
    fileID = int(data_json['fileID'])
    file=File.objects.get(fileID=fileID)
    info = file.info()
    content = file.content()
    if file.is_dir():
        result = {'sonList': content}
    else:
        result = content
    file.last_visit_time = datetime.datetime.now()
    file.save()
    info.update(result)
    return good_res('成功读取文件', info)


@csrf_exempt
def project_to_team(request):
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    data_json = json.loads(request.body)
    fileID = int(data_json['fileID'])
    file=File.objects.get(fileID=fileID)
    tu_list = Team_User.objects.filter(team=file.team)
    userList = [
        {
            'username': tu.user.username,
            'email': tu.user.email,
            'userID': tu.user.userID,
            'authority': tu.authority,
            'avatar':tu.user.avatar
        }
        for tu in tu_list
    ]
    return good_res('成功获取团队列表', {'userList':userList,'teamID':file.team.teamID})


@csrf_exempt
def common_template_prototype_read(request):
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    file=File.objects.get(fileID=268)
    son_list = File.objects.filter(father=file,type=13)
    return good_res('成功读取原型图模板', {'prototypeList':[x.prototype_info() for x in son_list if not x.is_deleted]})

@csrf_exempt
def a(request):
    file_list=File.objects.filter(team=None)
    for file in file_list:
        file.delete()
    return good_res('操作成功')


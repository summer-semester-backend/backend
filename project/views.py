import datetime
from jwt import encode
from user.models import User
from .models import Project
from team.models import Team, Team_User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.responce import res, good_res, warning_res, error_res
from utils.responce import method_err_res, not_login_res, bad_authority_res
from utils.params import lack_error_res, check_lack, get_params
from utils.utils import get_user_id, random_str, get_user_auth
from django.core.mail import send_mail
from backend import settings


@csrf_exempt
def create_project(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'projectName', 'teamID', 'projectImage')
    vals['userID'] = userID
    if not vals['projectImage']:
        vals['projectImage'] = 'https://www.bing.com/images/search?view=detailV2&ccid=zuIP14j9&id' \
                               '=2393853412087C812330763AE8F8742514E8BA40&thid=OIP.zuIP14j9CU1p0nXGr2FshgHaE7&mediaurl' \
                               '=https%3A%2F%2Fimg3.qianzhan.com%2Fnews%2F202010%2F29%2F20201029' \
                               '-96992a2ccc4beb54_700x5000.jpg&exph=466&expw=700&q=%e9%a1%b9%e7%9b%ae&simid' \
                               '=607986435445885181&form=IRPRST&ck=1F07A890F2368D13B9E4DDEF87F3FC65&selectedindex=18' \
                               '&ajaxhist=0&ajaxserp=0&vt=0&sim=11 '
    # 项目名不可为空
    if len(vals['projectName']) == 0:
        return error_res('项目名不可为空')
    # 项目名不可重复
    project_list = Project.objects.filter(project_name=vals['projectName'])
    if len(project_list) > 0:
        return error_res('项目名已存在')
    user = User.objects.get(userID=vals['userID'])
    team = Team.objects.get(teamID=vals['teamID'])
    project = Project(
        project_name=vals['projectName'],
        project_creator=user,
        team=team,
        project_image=vals['projectImage']
    )
    project.save()
    return res(0, '项目创建成功', {'projectID': project.projectID})


@csrf_exempt
def delete_project(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'projectID')
    vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_error_res(lack_list)
    # 项目名不可为空
    if len(vals['projectID']) == 0:
        return error_res('项目名不可为空')
    # 项目不存在
    project_list = Project.objects.filter(projectID=vals['projectID'])
    if len(project_list) == 0:
        return error_res('项目名不存在')
    project = Project.objects.get(projectID=vals['projectID'])
    project.delete()
    return res(0, '项目删除成功')


@csrf_exempt
def project_rename(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'projectID', 'newProjectName')
    vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_error_res(lack_list)
    # 项目名不可为空
    if len(vals['newProjectName']) == 0:
        return error_res('项目名不可为空')
    # 项目名不可重复
    project_list = Project.objects.filter(project_name=vals['newProjectName'])
    if len(project_list) > 0:
        return error_res('项目名已存在')
    project = Project.objects.get(projectID=vals['projectID'])
    project.project_name = vals['newProjectName']
    project.save()
    return res(0, '项目重命名成功')


@csrf_exempt
def project_detail(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'projectID')
    vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_error_res(lack_list)
    # 项目不可为空
    if len(vals['projectID']) == 0:
        return error_res('项目不存在')
    # 项目名不可重复
    project_list = Project.objects.filter(project_name=vals['newProjectName'])
    if len(project_list) == 0:
        return error_res('项目不存在')
    project = Project.objects.get(projectID=vals['projectID'])
    project.last_visit_time = datetime.datetime.now()
    project.save()
    content = {'projectID': project.projectID, 'projectName': project.project_name,
               'projectImage': project.project_image, 'teamName': project.team.team_name,
               'userName': project.project_creator.username, 'createTime': project.create_time,
               'lastVisitTime': project.last_visit_time}
    return res(0, '项目重命名成功', content)


@csrf_exempt
def project_list_user(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    project_list = Project.objects.filter(is_activate=1)
    result_list = []
    for project in project_list:
        user_list = Team_User.objects.filter(team=project.team)
        for user in user_list:
            if user.user.authority >= 0 and user.user.userID == userID:
                content = {'projectID': project.projectID, 'projectName': project.project_name,
                           'projectImage': project.project_image, 'createTime': project.create_time,
                           'lastVisitTime': project.last_visit_time}
                result_list.append(content)
                break
    content = {'list': result_list}
    return res(0, '查询成功', content)


@csrf_exempt
def project_list_user_team(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'teamID')
    vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_error_res(lack_list)
    team_list = Team.objects.filter(teamID=vals['teamID'])
    if len(team_list) == 0:
        return error_res('团队不存在')
    team = Team.objects.get(teamID=vals['teamID'])
    project_list = Project.objects.filter(team=team, is_active=1)
    result_list = []
    for project in project_list:
        content = {'projectID': project.projectID, 'projectName': project.project_name,
                   'projectImage': project.project_image, 'createTime': project.create_time,
                   'lastVisitTime': project.last_visit_time}
        result_list.append(content)
    content = {'list': result_list}
    return res(0, '查询成功', content)


@csrf_exempt
def project_last_visit(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request)
    vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_error_res(lack_list)
    user = User.objects.get(userID=userID)
    project_list = Project.objects.filter(is_active=1).order_by('-last_visit_time')
    result_list = []
    for project in project_list:
        if get_user_auth(user, project.team) >= 0:
            content = {'projectID': project.projectID, 'projectName': project.project_name,
                       'projectImage': project.project_image, 'createTime': project.create_time,
                       'lastVisitTime': project.last_visit_time}
        result_list.append(content)
    content = {'list': result_list}
    return res(0, '查询成功', content)


@csrf_exempt
def abandon_project(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'projectID')
    vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_error_res(lack_list)
    # 项目名不可为空
    if len(vals['projectID']) == 0:
        return error_res('项目名不可为空')
    # 项目不存在
    project_list = Project.objects.filter(projectID=vals['projectID'])
    if len(project_list) == 0:
        return error_res('项目名不存在')
    project = Project.objects.get(projectID=vals['projectID'])
    project.is_active = 0
    project.abandon_time = datetime.datetime.now()
    project.save()
    return res(0, '项目删除成功')


@csrf_exempt
def project_list_user_bin(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    project_list = Project.objects.filter(is_activate=0)
    result_list = []
    for project in project_list:
        user_list = Team_User.objects.filter(team=project.team)
        for user in user_list:
            if user.user.authority >= 0 and user.user.userID == userID:
                content = {'projectID': project.projectID, 'projectName': project.project_name,
                           'abandonTime': project.abandon_time, 'teamName': project.team.team_name}
                result_list.append(content)
                break
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
    project_list = Project.objects.filter(is_activate=0)
    for project in project_list:
        user_list = Team_User.objects.filter(team=project.team)
        for user in user_list:
            if user.user.authority >= 0 and user.user.userID == userID:
                project.delete()
                break
    return res(0, '回收站已清空')


@csrf_exempt
def recover_project(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'projectID')
    vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_error_res(lack_list)
    # 项目名不可为空
    if len(vals['projectID']) == 0:
        return error_res('项目名不可为空')
    # 项目不存在
    project_list = Project.objects.filter(projectID=vals['projectID'])
    if len(project_list) == 0:
        return error_res('项目名不存在')
    project = Project.objects.get(projectID=vals['projectID'])
    project.is_active = 1
    project.save()
    return res(0, '项目恢复成功')

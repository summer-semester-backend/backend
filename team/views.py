from django.shortcuts import render

from user.models import User
from .models import Team, Team_User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.responce import good_res, warning_res, error_res, method_err_res, not_login_res
from utils.params import lack_error_res, check_lack, get_params
from utils.utils import get_user_id, get_user_auth


@csrf_exempt
def create_team(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'teamName')
    vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        return lack_error_res(lack_list)
    # 团队名不可为空
    if len(vals['team_name']) == 0:
        return error_res('团队名不可为空')
    # 团队名不可重复
    team_list = Team.objects.filter(team_name=vals['team_name'])
    if len(team_list) > 0:
        return error_res('团队名已存在')
    # 获取本用户
    user = User.objects.get(userID=vals['userID'])
    # # 生成团队根文件
    # root_file = File(
    #     fatherID=-1,
    #     isDir=True,
    #     file_name='root',
    #     commentFul=False,
    #     isDelete=False,
    # )
    # root_file.save()
    # 设置团队
    team = Team(
        team_name=vals['teamName'],
        creator=user,
        # team_root_file=root_file
    )
    team.save()
    Team_User.objects.create(user=user, team=team, authority=2)
    return good_res("创建团队成功")




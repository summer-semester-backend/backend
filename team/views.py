import datetime

from django.shortcuts import render
from jwt import encode

from user.models import User
from .models import Team, Team_User, C, Invitation
from file.models import File, FType
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.responce import res, good_res, warning_res, error_res
from utils.responce import method_err_res, not_login_res, bad_authority_res
from utils.params import lack_error_res, lack_check, get_params
from utils.utils import get_user_id, get_user_auth, random_str, user_simple_info, get_user
from .tools import general_check

from django.core.mail import send_mail

from backend import settings


def create_team_implement(user, team_name, summary):
    if len(team_name) == 0:
        return error_res('团队名不可为空')
    # 团队名不可重复
    # team_list = Team.objects.filter(team_name=team_name)
    # if len(team_list) > 0:
    #     return error_res('团队名已存在')
    root_file = File.objects.create(
        file_creator=user,
        file_image='',
        file_name='root',
        type=FType.root,
    )
    team = Team(
        team_name=team_name,
        creator=user,
        summary=summary,
        root_file=root_file
    )
    team.save()
    root_file.team = team
    root_file.save()
    Team_User.objects.create(user=user, team=team, authority=2)
    return res(0, '成功创建团队', {'teamID': team_name})



@csrf_exempt
def create_team(request):
    # 一般检查
    if request.method != 'POST':
        return method_err_res()
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    # 获取信息，并检查是否缺项
    vals = get_params(request, 'teamname', 'summary')
    vals['userID'] = userID
    lack, lack_list = lack_check(vals)
    if lack:
        return lack_error_res(lack_list)
    # 团队名不可为空
    if len(vals['teamname']) == 0:
        return error_res('团队名不可为空')
    # 团队名不可重复
    team_list = Team.objects.filter(team_name=vals['teamname'])
    if len(team_list) > 0:
        return error_res('团队名已存在')
    # 获取本用户
    user = get_user(request)
    if user is None:
        return error_res('找不到本用户?')
    return create_team_implement(user, vals['teamname'], vals['summary'])



@csrf_exempt
def get_detail(request):
    check = general_check(request, 'POST', ['teamID'], C.member)
    if not check['success']:
        return check['res']
    user = check['user']
    team = check['team']
    return good_res('成功获取团队信息', {
        'teamname': team.team_name,
        'summary': team.summary,
    })



@csrf_exempt
def get_users_info(request):
    check = general_check(request, 'POST', ['teamID'], C.member)
    if not check['success']:
        return check['res']
    # user = check['user']
    team = check['team']
    tu_list = Team_User.objects.filter(team=team)
    userList = list(map(lambda tu: {
        'username': tu.user.username,
        'email': tu.user.email,
        'userID': tu.user.userID,
        'authority': tu.authority,
    }, tu_list))
    return good_res('成功获取团队列表', {'userList':userList})
    # content = {'managerList': [], 'userList': [], 'invalidList': []}
    # founder = Team_User.objects.get(team=team, authority=C.founder)
    # content['managerList'].append(user_simple_info(founder.user))
    # manager_list = Team_User.objects.filter(team=team, authority=C.manager)
    # user_list = Team_User.objects.filter(team=team, authority=C.member)
    # invited_list = Team_User.objects.filter(team=team, authority=C.invited)
    # content['managerList'] += map(lambda x: user_simple_info(x.user), manager_list)
    # content['userList'] += map(lambda x: user_simple_info(x.user), user_list)
    # content['invalidList'] += map(lambda x: user_simple_info(x.user), invited_list)
    # return good_res('成功获取团队成员信息', content)


@csrf_exempt
def add_manager(request):
    check = general_check(request, 'POST', ['teamID', 'userID'], C.founder)
    if not check['success']:
        return check['res']
    team = check['team']
    that_user_id = check['vals']['userID']
    that_user = User.objects.get(userID=that_user_id)
    # 此用户必须是团队普通成员
    auth = get_user_auth(that_user, team)
    if auth == C.manager:
        return warning_res('此用户已经是团队管理员')
    if auth != C.member:
        return error_res('此用户不是本团队的普通成员')
    tu = Team_User.objects.filter(user=that_user, team=team)
    assert len(tu) == 1
    tu = tu[0]
    tu.authority = C.manager
    tu.save()
    return good_res('成功将'+that_user.username+'设为管理员')


@csrf_exempt
def change_team_info(request):
    check = general_check(request, 'POST', ['teamID', 'summary'], C.manager)
    if not check['success']:
        return check['res']
    team = check['team']
    summary = check['vals']['summary']
    team.summary = summary
    team.save()
    return good_res('成功修改团队信息')


@csrf_exempt
def invite(request):
    check = general_check(request, 'POST', ['teamID', 'email'], C.manager)
    if not check['success']:
        return check['res']
    team = check['team']
    email = check['vals']['email']
    # that_user_id = check['vals']['userID']
    try:
        that_user = User.objects.get(email=email)
    except:
        return error_res('邮箱有问题')
    # 被邀请人现在不能在团队中
    auth = get_user_auth(that_user, team)
    if auth > C.invited:
        print(auth)
        return warning_res('用户'+that_user.username+'已经在团队中')
    # 生成邀请链接
    s = random_str(20)
    url = 'http://43.138.77.8:8000/api/team/acceptInvitation/' + s
    print(url)
    Invitation.objects.create(user=that_user, team=team, invite_url=s)
    send_status = send_mail(
        subject='加入团队邀请 - '+team.team_name,
        message='访问链接以加入:'+url,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email])
    tu = Team_User.objects.filter(team=team, user=that_user)
    if len(tu) == 1:
        tu[0].authority = C.invited
        tu[0].save()
    elif len(tu) == 0:
        Team_User.objects.create(team=team, user=that_user, authority=C.invited)
    else:
        raise Exception('Team_User中有多个权限信息')
    return good_res('已发出邀请邮件')


@csrf_exempt
def accept_invitation(request):
    print(request.get_host() + request.get_full_path())
    s = request.get_full_path()[-20:]
    invitation = Invitation.objects.filter(invite_url=s)
    if len(invitation) != 1:
        return
    invitation = invitation[0]
    user = invitation.user
    team = invitation.team
    tu = Team_User.objects.get(user=user, team=team)
    if tu.authority == C.invited:
        tu.authority = C.member
    tu.save()
    invitation.delete()
    return good_res('用户'+user.username+'已加入')

    # Team_User.objects.create(user=user, team=team, authority=C.member)


@csrf_exempt
def delete_manager(request):
    check = general_check(request, 'POST', ['teamID', 'userID'], C.founder)
    if not check['success']:
        return check['res']
    team = check['team']
    that_user_id = check['vals']['userID']
    that_user = User.objects.get(userID=that_user_id)
    # 此用户必须为团队管理员
    if get_user_auth(that_user, team) != 1:
        return warning_res('用户'+that_user.username+'不是团队的管理员')
    tu = Team_User.objects.filter(user=that_user, team=team)
    assert len(tu) == 1
    tu = tu[0]
    tu.authority = C.member
    tu.save()
    return good_res('用户'+that_user.username+'已是普通成员')
    # email = check['vals']['email']


@csrf_exempt
def delete_team(request):
    check = general_check(request, 'POST', ['teamID'], C.founder)
    if not check['success']:
        return check['res']
    team = check['team']
    team.delete()
    return good_res('团队'+team.team_name+'已经被销毁')


@csrf_exempt
def delete_member(request):
    check = general_check(request, 'POST', ['teamID','userID'], C.manager)
    if not check['success']:
        return check['res']
    team = check['team']
    me = check['user']
    that_user_id = check['vals']['userID']
    that_user = User.objects.get(userID=that_user_id)
    that_user_auth = get_user_auth(that_user, team)
    my_auth = get_user_auth(me, team)
    if that_user_auth < C.invited:
        return warning_res('对方不在团队中')
    if that_user_auth >= my_auth:
        return error_res('由于你的权限不比对方高, 你无法踢出他')
    tu = Team_User.objects.get(user=that_user, team=team)
    tu.delete()
    return good_res('已将用户'+that_user.username+'踢出')


@csrf_exempt
def my_team_list(request):
    b, userID = get_user_id(request)
    if not b:
        return not_login_res()
    user = User.objects.get(userID=userID)
    tu_list = Team_User.objects.filter(user=user)
    team_list = []
    for tu in tu_list:
        dic = tu.team.info()
        dic['authority'] = C.trans(tu.authority)
        team_list.append(dic)
    return good_res('成功获取我所在的团队信息', {'list': team_list})


@csrf_exempt
def leave(request):
    check = general_check(request, 'POST', ['teamID'], C.invited)
    if not check['success']:
        return check['res']
    team = check['team']
    user = check['user']
    if get_user_auth(user, team) == C.founder:
        return error_res('创建者不能退出团队')
    tu = Team_User.objects.get(team=team, user=user)
    tu.delete()
    return good_res('已退出团队')
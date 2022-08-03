from .models import Team, Team_User, C
from user.models import User
from utils.responce import res, good_res, warning_res, error_res
from utils.responce import method_err_res, not_login_res, bad_authority_res
from utils.params import lack_error_res, check_lack, get_params, get_params_by_list
from utils.utils import get_user_id, get_user_auth

def id_to_team(teamID):
    assert isinstance(teamID, str)
    try:
        team = Team.objects.get(team_name=teamID)
    except:
        return None
    return team


def general_check(request, method, params, authority):
    """团队操作的各种检查, 如果检查无误则返回参数dict 用户对象 团队对象
    request 传入的请求
    method 希望的请求方法
    params 需要那些参数
    authority 操作需要的权限
    """
    assert isinstance(method, str)
    assert isinstance(params, list)
    assert isinstance(authority, int)
    result = {'success':False}
    # 方法检查
    if request.method != method:
        result['res'] = method_err_res()
        return result
    b, userID = get_user_id(request)
    if not b:
        result['res'] = not_login_res()
        return result
    # 获取信息，并检查是否缺项
    vals = get_params_by_list(request, params)
    # vals['userID'] = userID
    lack, lack_list = check_lack(vals)
    if lack:
        result['res'] = lack_error_res(lack_list)
        return result
    # 获取本用户
    user = User.objects.get(userID=userID)
    team = id_to_team(vals['teamID'])
    if team is None:
        result['res'] = error_res('团队id不存在')
        return result
    auth = get_user_auth(user, team)
    # 权限检查
    if auth < authority:
        result['res'] = bad_authority_res('此操作需要权限'+str(authority)+', 你的权限为'+str(auth))
        return result
    result['success'] = True
    result['vals'] = vals
    result['user'] = user
    result['team'] = team
    return result
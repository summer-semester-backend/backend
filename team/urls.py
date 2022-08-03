from django.urls import path, re_path
from .views import *
urlpatterns = [
    # 指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('create', create_team),
    path('detail', get_detail),
    path('users', get_users_info),
    path('manager/add', add_manager),
    path('change', change_team_info),
    path('user/invite', invite),
    re_path('acceptInvitation/.*', accept_invitation),
    path('manager/delete', delete_manager),
    path('delete', delete_team),
    path('user/delete', delete_member),
    path('list', my_team_list),
    path('leave', leave),
    # path('')
    # path('myTeams', my_team_list),
    # path('teamInfo', team_info),
    # path('invite', invite),
    # path('kick', kick),
    # path('destroy', destroy),
    # path('rename', rename),
    # path('debugAllTeam', debug_all_team),

    # path('leaveTeam', leave_team),
    # path('is_manager', is_manager),
    # path('manager_transfer', manager_transfer),
    # path('debugClearTeam', debug_clear_team),
]
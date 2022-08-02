from django.urls import path
from .views import *
urlpatterns = [
    # 指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('create', create_team),

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
from django.urls import path, re_path
from .views import *
urlpatterns = [
    # 指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('createProject', create_project),
    path('deleteProject', delete_project),
    path('renameProject', project_rename),
    path('projectDetail', project_rename),
    path('userProjectList', project_list_user),
    path('teamProjectList', project_list_user_team),
    path('lastVisitProject', project_last_visit),
]
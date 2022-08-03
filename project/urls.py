from django.urls import path
from .views import *
urlpatterns = [
    path('createProject', create_project),
    path('deleteProject', delete_project),
    path('renameProject', project_rename),
    path('projectDetail', project_rename),
    path('userProjectList', project_list_user),
    path('teamProjectList', project_list_user_team),
    path('lastVisitProject', project_last_visit),
    path('abandonProject', abandon_project),
    path('recoverProject', recover_project),
    path('projectUserBinList', project_list_user_bin),
    path('clearBin', clear_bin),
]
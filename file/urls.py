from django.urls import path, re_path
from .views import *

urlpatterns = [
    # 指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('create', create),
    path('read', read),
    path('write', write),
    path('delete', delete_file),
    path('recover', recover_file),
    path('recently', project_last_visit),
    path('binList', bin_list),
    path('clearBin', clear_bin),
    path('all', all),
    path('centerRead', center_read),
    path('copy', copy),
    path('ancestor',ancestor),
    path('commonTemplate',common_template_text_read),
    path('teamTemplate',template_read),
    path('createTemplate',create_template),
    path('commonRead',common_read),
    path('projectToTeam',project_to_team),
    path('commonPrototypeTemplate',common_template_prototype_read),
    path('a',a),
    path('sharePrototype', share),
    path('closeSharePrototype', close_share),
    path('commonRead',common_read),

    path('acquireLock', acquire_lock),
    path('releaseLock', release_lock),
    path('keepLock', keep_lock),
]


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
]


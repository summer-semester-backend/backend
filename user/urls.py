from django.urls import path
from .views import *

urlpatterns = [
    path('put', put),
    path('delete', delete),
    path('get', get),
    path('post', post),
    path('login', login),
    path('register', register),
    path('email_register', email_register),
    path('email_forget', email_forget),
    path('password_forget', password_forget),
    path('password_change', password_change),
    path('upload_info', upload_info),
    path('upload_avatars', upload_avatars),
    path('get_user', get_user),
]

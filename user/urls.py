from django.urls import path
from .views import *

urlpatterns = [
    path('search', search),
    path('login', login),
    path('register', register),
    path('emailRegister', email_register),
    path('emailForget', email_forget),
    path('forgetPassword', password_forget),
    path('changePassword', password_change),
    path('update', update),
    path('detail', get_user),
    path('upload', upload),
    path('update_ava', update_ava)
]

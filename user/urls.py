from django.urls import path
from .views import *

urlpatterns = [
    path('hello', hello),
    path('put', put),
    path('delete', delete),
    path('get', get),
    path('post', post),
    path('yoo', yoo),
    path('login', login),
]

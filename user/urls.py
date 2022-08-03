from django.urls import path
from .views import *

urlpatterns = [
    path('put', put),
    path('delete', delete),
    path('get', get),
    path('post', post),
    path('search', search),
]

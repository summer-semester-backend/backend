from django.urls import path
from .views import *

urlpatterns = [
    path('hello', hello),
    path('yoo', yoo),
    path('login', login),
]

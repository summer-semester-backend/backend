from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from utils.utils import *

@csrf_exempt
def hello(request):
    print("小学期!")

@csrf_exempt
def yoo(request):
    return JsonResponse({'msg':'yoo!'})

@csrf_exempt
def login(request):
    params = post_get_all(request, 'username', 'password')
    lack, lack_list = check_lack(params)
    if lack:
        return lack_err(lack_list)
    return JsonResponse({
        'username': params['username'],
        'password': params['password'],
    })

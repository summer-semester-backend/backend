import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict, JsonResponse


@csrf_exempt
def put(request):
    if request.method == 'PUT':
        a = QueryDict(request.body)
        s = list(a.items())[0][0]
        print(s)
        print(type(s))
        data_json = json.loads(request.body)
        print(data_json)
        key = data_json['key']
        field = data_json['field']
        print(key, field)
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def delete(request):
    if request.method == 'DELETE':
        a = QueryDict(request.body)
        s = list(a.items())[0][0]
        print(s)
        print(type(s))
        data_json = json.loads(request.body)
        print(data_json)
        key = data_json['key']
        field = data_json['field']
        print(key, field)
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def get(request):
    if request.method == 'GET':
        key = request.GET.get('key')
        field = request.GET.get('field')
        print(key, field)
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


@csrf_exempt
def post(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        field = request.POST.get('field')
        print(key, field)
        result = {'result': 0, 'message': '前端炸了!'}
        return JsonResponse(result)


from backend.utils.utils import *


@csrf_exempt
def hello(request):
    print("小学期!")


@csrf_exempt
def yoo(request):
    return JsonResponse({'msg': 'yoo!'})


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

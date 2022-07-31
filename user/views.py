from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def hello(request):
    print("小学期!")

@csrf_exempt
def yoo(request):
    return JsonResponse({'msg':'yooo!'})

import json
from django.http import HttpRequest, JsonResponse


# 一次性get所有参数, args为可变参数列表
def get_params(request, *args):
    assert isinstance(request, HttpRequest)
    data_json = json.loads(request.body)
    result = {}
    for arg in args:
        result[str(arg)] = result[str(arg)]
    return result


# 检查一个字典中是否有none
def check_lack(obj_dic):
    lack_list = []
    for key, obj in obj_dic.items():
        if obj is None:
            lack_list.append(key)
    if len(lack_list) > 0:
        return True, lack_list
    return False, None


# 传过来的数据存在缺项
def lack_error_res(lack_list):
    return JsonResponse({
        'result': 2,
        'message': '请求缺少字段',
        'lack_list': list(lack_list),
    })
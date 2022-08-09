# 各种用来构建返回值的函数

from django.http import JsonResponse


def res(code, message, content=None):
    assert content is None or isinstance(content, dict)
    assert isinstance(message, str)
    r = {'result': code, 'message': message}
    if content is None:
        return JsonResponse(r)
    for key in content:
        r[key] = content[key]
    return JsonResponse(r)


def good_res(message, content=None):
    return res(0, message, content)


def warning_res(message, content=None):
    return res(1, message, content)


def error_res(message, content=None):
    return res(2, message, content)


def method_err_res():
    return error_res('请求方法错误')


def not_login_res():
    r = {'result': 10, 'message': 'Token有误！'}
    return JsonResponse(r)


def bad_authority_res(want_to_do_what):
    return error_res("操作权限不足: "+str(want_to_do_what))


def resource_not_found_res():
    return res(11, "资源不存在或者没有权限访问")

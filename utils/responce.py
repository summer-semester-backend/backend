from django.http import JsonResponse


def res(code, message, content):
    assert content is None or type(content) == 'dict'
    assert type(message) == 'str'
    r = {'result': code, 'message': message}
    for key in content:
        r[key] = content[key]
    return JsonResponse(r)


def good_res(message, content=None):
    return res(0, message, content)


def warning_res(message, content=None):
    return res(1, message, content)


def error_res(message, content=None):
    return res(2, message, content)

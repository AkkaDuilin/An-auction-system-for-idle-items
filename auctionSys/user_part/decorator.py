from django.http import HttpResponseRedirect
from django.contrib import messages


def login(func):
    def wrapper(request, *args, **kw):
        if request.session.has_key('user_id'):
            return func(request, *args, **kw)
        else:
            messages.error(request, '请先登录')
            res = HttpResponseRedirect('/user/login/')
            res.set_cookie('url', request.get_full_path())
            return res
    return wrapper

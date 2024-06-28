from functools import wraps
from django.http import HttpResponseForbidden, HttpResponseRedirect

def user_is_authenticated(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        is_auth = request.session.get('is_authenticated', False)
        if is_auth:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')  # Redirect to login page if not authenticated
    return wrap

def user_is_admin(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.session.get('role') == 'admin':  # 'admin' corresponds to 'Admin'
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access restricted: Only administrators are allowed to access this page.")
    return wrap

def user_is_author(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.session.get('role') == 'author':  # 'author' corresponds to 'Author'
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access restricted: Only authors are allowed to access this page.")
    return wrap

def user_is_regular(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.session.get('role') == 'regular':  # 'regular' corresponds to 'Regular User'
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to view this page.")
    return wrap

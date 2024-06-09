from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect
from functools import wraps
from django.core.exceptions import PermissionDenied

def RequiredSuperuser(func):
    ## Limit view to superusers only
    def checkSuperuser(request, *args, **kwargs):
        if not request.user.is_superuser:
            print('access denied...')
            raise PermissionDenied # error 403
        return func(request, *args, **kwargs)
    return checkSuperuser

def RequiredGroupOrSuperuser(group_names):
    def _check_group(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            print(request.user)
            if (not (request.user.groups.filter(name__in=group_names).exists()) or request.user.is_superuser):
                return redirect('/login/')
                #raise Http404
            return func(request, *args, **kwargs)
        return wrapper
    return _check_group
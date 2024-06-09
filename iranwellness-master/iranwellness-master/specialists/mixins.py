from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class GroupRequiredMixin(object):
    group_required = None ### list of strings, required param
    def dispatch(self, request, *args, **kwargs):
      user_groups = []
      for group in request.user.groups.values_list('name', flat=True):
        user_groups.append(group)
      if len(set(user_groups).intersection(self.group_required)) <= 0:
        logout(request)
        return redirect('/login/')
      return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)

class GroupOrSuperuserRequiredMixin(object):
    group_required = None ### list of strings, required param
    def dispatch(self, request, *args, **kwargs):
      user_groups = []
      for group in request.user.groups.values_list('name', flat=True):
        user_groups.append(group)
      if (len(set(user_groups).intersection(self.group_required)) <= 0 and (not request.user.is_superuser)):
        logout(request)
        return redirect('/login/')
      return super(GroupOrSuperuserRequiredMixin, self).dispatch(request, *args, **kwargs)
from rest_framework.permissions import BasePermission, IsAdminUser
from django.contrib.auth.models import Group


class IsSuperUser(IsAdminUser):
    message = 'با عرض پوزش دسترسی به این ویو برای شما مجاز نیست!'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class GroupBasePermission(BasePermission):
    message = 'با عرض پوزش دسترسی به این ویو برای شما مجاز نیست!'

    def has_permission(self, request, view):
        ##
        user = request.user
        ##
        required_groups = getattr(view, "required_groups", [])
        if not required_groups:
          self.message = 'گروه‌های مجاز به استفاده از این ویو مشخص نشده‌اند!'
          return False
        return user.groups.filter(name__in=required_groups).exists()


class IsObjectOwner(BasePermission):
    message = 'با عرض پوزش دسترسی به این ویو برای شما مجاز نیست!'
    
    def has_object_permission(self, request, view, obj):
        ## get user
        user = request.user
        ## check object owner
        if (obj.user == user):
          return True
        return False

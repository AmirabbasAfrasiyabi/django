from django.contrib import admin
from .models import  *



@admin.register(dayoff)
class dayoffAdmin(admin.ModelAdmin):
    list_display = ('day','month','year')
    list_filter = ('year','month')


@admin.register(healthreservation)
class healthreservationAdmin(admin.ModelAdmin):
    list_display = ('string','get_user',)
    search_fields = ('string','user__profiledb__firstname','user__profiledb__lastname')
    def get_user(self,obj):
        return (obj.user.profiledb.firstname + ' ' + obj.user.profiledb.lastname)


@admin.register(resonancereservation)
class resonancereservationAdmin(admin.ModelAdmin):
    list_display = ('string','get_user',)
    search_fields = ('string','user__profiledb__firstname','user__profiledb__lastname')
    def get_user(self,obj):
        return (obj.user.profiledb.firstname + ' ' + obj.user.profiledb.lastname)

from django.contrib import admin
from authapp.models import *

##### sms verification
class sms_verificationAdmin(admin.ModelAdmin):
    list_display = ('ip','phone_number','time')
admin.site.register(sms_verification_table,sms_verificationAdmin)

##### profile
@admin.register(profiledb)
class profiledbAdminModel(admin.ModelAdmin):
    list_display = ('user','firstname','lastname')
    search_fields= ('user__username','firstname','lastname')

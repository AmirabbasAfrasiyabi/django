from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from ticket.models import *



class ChatModelInline(GenericTabularInline):
    model = Chat
    extra = 0


@admin.register(TicketOnServices)
class TicketOnServicesAdmin(admin.ModelAdmin):
    list_display = ['user','service','status']
    list_filter = ['service','status']
    inlines = [ChatModelInline]
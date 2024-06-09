from django.urls import path
from ticket.views import *

urlpatterns = [
    path('', ticket_list),
    path('newticket/', NewTicket),
    path('<int:id>/', ticket_detail),
    path('<int:id>/closeticket/', closeticket),
]

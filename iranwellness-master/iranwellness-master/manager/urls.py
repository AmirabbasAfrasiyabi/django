from django.urls import path, include
from .views import *

app_name = 'manager'


urlpatterns = [
    path('', ManagerDashboard.as_view()),
    
    ######################################################
    #######      USERS
    ######################################################
    path('users/', UsersListView.as_view(), name='users-list'),
    path('users/add/', AddUserView.as_view(), name='add-user'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    
    ######################################################
    #######      RESERVATION
    ######################################################
    path('updatecalendar/', UpdateCalendar.as_view()),
    path('monthinfo/<int:idx>/', MonthinfoManager.as_view()),
    ##
    path('reservation/', ReservationOption.as_view(), name='reservation'),
    path('services/<str:reserveType>/', ManagerDayChoose.as_view()),
    path('services/searchreserve/<int:year>/<int:month>/<int:day>/', ListView.as_view()),
    ##
    path('reservation/services/', ChooseReservationService.as_view()),
    path('services/<str:reserveType>/queueHealth/', ManagerDayChoose.as_view()),
    path('services/newreserve/queueHealth/<int:year>/<int:month>/<int:day>/',TimeChooseM.as_view()),
    path('services/newreserve/queueHealth/<int:year>/<int:month>/<int:day>/<int:duration>',Search.as_view()),
    path('services/newreserve/queueHealth/<int:year>/<int:month>/<int:day>/<int:duration>/<int:order>',ResultM.as_view()),
    ##
    path('services/<str:reserveType>/queueResonance/', ManagerDayChoose.as_view()),
    path('services/newreserve/queueResonance/<int:year>/<int:month>/<int:day>/',TimeChooseM.as_view()),
    path('services/newreserve/queueResonance/<int:year>/<int:month>/<int:day>/<int:duration>',Search.as_view()),
    path('services/newreserve/queueResonance/<int:year>/<int:month>/<int:day>/<int:duration>/<int:order>',ResultM.as_view()),

    ######################################################
    #######      QUIZ
    ######################################################
    path('quizsearchManager/',QuizSearchManager.as_view()),

    ######################################################
    #######      TICKETS
    ######################################################
    path('tickets/', Tickets.as_view()),
    path('tickets/<int:id>/', DetailTicket.as_view(), name='ticket-detail'),

    ######################################################
    #######      RECEIPT
    ######################################################
    path('receipt/',Receipt.as_view()),

    ######################################################
    path('api/', include('manager.api_urls')),
    
]


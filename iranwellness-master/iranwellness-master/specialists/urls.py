from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = 'specialists'

urlpatterns = [
  path('', SpecialistsDashboard.as_view()),
  
  ## USERS
  path('users/', UsersListView.as_view(), name='users-list'),
  path('users/change/<int:id>/', UsersDetailView.as_view(), name='user-detail'),
  
  ## RESERVATION
  path('reservasion/', ServicesListView.as_view()),
  path('reservasion/<str:service>/', ReservationDayChooseView.as_view()),
  path('reservasion/<str:service>/<int:year>/<int:month>/<int:day>/', ReservsListView.as_view()),
  
  ## آنالیزها
  path('analysis/',analysislist),
  path('analysis/quizResultRoutesItems/', quizResultItems),
  path('analysis/quizResultRoutesItems/<int:number>/', quizSubmittedList),
  path('analysis/quizResultRoutesItems/<int:number>/<int:pk>/', quizsearchSpecialists),

  path('analysis/<str:name>/', analysisoptions),
  path('analysis/<str:name>/submitAnalysis/', uploadfilelist),
  path('analysis/<str:name>/submitAnalysis/<int:pk>/', uploadfile.as_view()),
  path('analysis/<str:name>/editAnalysis/chooseUser/', chooseUserforEditAnalysis.as_view()),
  path('analysis/<str:name>/editAnalysis/<str:username>/', editAnalysis.as_view()),
  
  ## پیگیری های
  path('tickets/', specialists_chooseServiceTickets.as_view()),
  path('tickets/<str:serviceSlug>/', specialist_list_tickets.as_view()),
  path('tickets/<str:serviceSlug>/<int:id>/', login_required(specialist_detail_ticket.as_view())),
]
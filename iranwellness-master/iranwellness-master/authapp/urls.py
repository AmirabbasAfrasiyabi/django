from django.urls import path, include
from .views import *


app_name = 'authapp'


urlpatterns = [
    
    path('api/', include('authapp.api_urls')),
    
]


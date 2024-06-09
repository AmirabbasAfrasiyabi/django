from django.urls import path, include
from rest_framework import routers
from .api_views import *

router = routers.SimpleRouter()
router.register(r'profiles', ProfileAPIViewset, basename='profiles')

urlpatterns = [
    path('', include(router.urls)),
]
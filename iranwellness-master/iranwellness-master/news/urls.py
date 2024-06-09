from django.urls import path
from news.views import *

urlpatterns = [
    path(r'', NewsList),
    path(r'<str:NewsName>/', NewsSubjectList),
    path(r'<str:NewsName>/<str:NewsSubject>/', NewsTopicList),
    path(r'<str:NewsName>/<str:NewsSubject>/<str:NewsTopic>/', NewsText)
]
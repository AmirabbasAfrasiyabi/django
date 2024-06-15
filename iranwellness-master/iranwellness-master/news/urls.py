from django.urls import path, re_path
from news.views import *

urlpatterns = [
    path('', NewsList, name='news_list'),
    re_path(r'^(?P<NewsName>[\w-]+)/$', NewsSubjectList, name='news_subject_list'),
    re_path(r'^(?P<NewsName>[\w-]+)/(?P<NewsSubject>[\w-]+)/$', NewsTopicList, name='news_topic_list'),
    re_path(r'^(?P<NewsName>[\w-]+)/(?P<NewsSubject>[\w-]+)/(?P<NewsTopic>[\w-]+)/$', NewsText, name='news_text'),
]
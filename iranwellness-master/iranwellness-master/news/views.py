from django.shortcuts import render, get_object_or_404, HttpResponse
from news.models import *

def NewsList(request):
    return HttpResponse("لیست موضوعات خبری از قبیل سلامتی در این صفحه بایستی نمایش داده شود.")

def NewsSubjectList(request, NewsName):
    news = get_object_or_404(new, Ename=NewsName)
    info = subject.objects.filter(new=news)
    context = {'info': info, 'news_name': NewsName}
    return render(request, 'news/NewsSubjectList.html', context)

def NewsTopicList(request, NewsName, NewsSubject):
    news = get_object_or_404(new, Ename=NewsName)
    subject_instance = get_object_or_404(subject, Ename=NewsSubject, new=news)
    info = topic.objects.filter(subject=subject_instance).order_by('order')
    context = {'info': info, 'news_name': NewsName, 'news_subject': NewsSubject}
    return render(request, 'news/NewsTopicList.html', context)

def NewsText(request, NewsName, NewsSubject, NewsTopic):
    news = get_object_or_404(new, Ename=NewsName)
    subject_instance = get_object_or_404(subject, Ename=NewsSubject, new=news)
    info = get_object_or_404(topic, subject=subject_instance, Ename=NewsTopic)
    context = {'info': info, 'news_name': NewsName, 'news_subject': NewsSubject, 'news_topic': NewsTopic}
    
    template_name = f'news/Htmldocs/{NewsName}-{NewsSubject}-{NewsTopic}.html'
    return render(request, template_name, context)

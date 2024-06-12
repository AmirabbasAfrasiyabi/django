from django.shortcuts import render, get_object_or_404, HttpResponse
from news.models import *

def NewsList(request):
    return render(request, 'news/index.html')

def NewsSubjectList(request, NewsName):
    news_instances = new.objects.filter(Ename=NewsName)
    if news_instances.exists():
        news = news_instances.first()  # استفاده از اولین رکورد پیدا شده
    else:
        news = get_object_or_404(new, Ename=NewsName)
    
    info = subject.objects.filter(new=news)
    context = {'info': info}
    return render(request, 'news/NewsSubjectList.html', context)

def NewsTopicList(request, NewsName, NewsSubject):
    news_instances = new.objects.filter(Ename=NewsName)
    if news_instances.exists():
        news = news_instances.first()  # استفاده از اولین رکورد پیدا شده
    else:
        news = get_object_or_404(new, Ename=NewsName)
    subject_instance = get_object_or_404(subject, Ename=NewsSubject, new=news)
    info = topic.objects.filter(subject=subject_instance).order_by('order')
    context = {'info': info}
    return render(request, 'news/NewsTopicList.html', context)

def NewsText(request, NewsName, NewsSubject, NewsTopic):
    news_instances = new.objects.filter(Ename='health')
    if news_instances.exists():
        news = news_instances.first()  # استفاده از اولین رکورد پیدا شده
    else:
        news = get_object_or_404(new, Ename='health')

    subject_instance = get_object_or_404(subject, Ename=NewsSubject, new=news)
    info = get_object_or_404(topic, subject=subject_instance, Ename=NewsTopic)
    context = {'info': info}
    
    template_name = 'news/Htmldocs/health-{}-{}.html'.format(NewsSubject, NewsTopic)
    return render(request, template_name, context)
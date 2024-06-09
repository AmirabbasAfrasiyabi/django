from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from news.models import *

def NewsList(request):
    return HttpResponse ("لیست موضوعات خبری از قبیل کرونا در این صفحه بایستی نمایش داده شود.")

def NewsSubjectList (request, NewsName):
    model = subject
    info = model.objects.filter(new = new.objects.get(Ename = NewsName))
    context = {'info': info}
    template_name = 'news/NewsSubjectList.html'
    return render (request, template_name, context)

def NewsTopicList (request, NewsName, NewsSubject):
    model   = topic
    NEWS    = new.objects.get(Ename = NewsName)
    SUBJECT = subject.objects.get(Ename = NewsSubject, new = NEWS)
    info    = model.objects.filter(subject=SUBJECT).order_by('order')
    if (info):
        context = {'info': info}
        template_name = 'news/NewsTopicList.html'
        return render(request, template_name, context)
    template_name = 'news/Htmldocs/'+ NewsName +'/'+ NewsSubject +'.html'
    context = {'info': SUBJECT}
    return render(request, template_name, context)

def NewsText (request, NewsName, NewsSubject, NewsTopic):
    NEWS    = new.objects.get(Ename = NewsName)
    SUBJECT = subject.objects.get(Ename = NewsSubject, new = NEWS)
    info = topic.objects.get(subject=SUBJECT, Ename = NewsTopic)
    template_name = 'news/Htmldocs/'+ NewsName +'/'+ NewsSubject +'-'+ NewsTopic +'.html'
    context = {'info': info}
    return render(request, template_name, context)
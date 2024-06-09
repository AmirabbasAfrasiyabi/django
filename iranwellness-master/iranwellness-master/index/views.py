from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from index.models import *
from authapp.models import profiledb

@login_required(redirect_field_name='', login_url='/login/')
def MSlogin(request):
    return render(request, 'manager/MSlogin.html')
    
@login_required(redirect_field_name='', login_url='/login/')
@csrf_exempt
def dashboard(request):
    template_name = "index/dashboard.html"
    if request.method == 'POST':
        displayStatus = request.POST.get('displayStatus')
        if (displayStatus == 'close'):
            request.session['Iranwellness-notif-COVID-19-open-status'] = request.user.username
            return HttpResponse(displayStatus)
        return HttpResponseForbidden()
    context = {'displayStatus':''}
    if (request.session.has_key('Iranwellness-notif-COVID-19-open-status') and request.session['Iranwellness-notif-COVID-19-open-status'] == request.user.username):
        context = {'displayStatus': 'close'}
    return render (request, template_name, context)
    
@login_required(redirect_field_name='', login_url='/login/')
def commentitems(request):
    user=request.user
    try:
        info= profiledb.objects.get(user=user)
        status= "valid"
    except ObjectDoesNotExist:
        status= "invalid"
    return render(request, 'index/CommentItems.html', {'status':status})

@login_required(redirect_field_name='', login_url='/login/')
def comments(request,item):
    if request.method=="POST":
        subject  = int(request.POST['subject'])
        branch   = int(request.POST['branch'])
        text     = request.POST['comment']
        comment.objects.create(user=request.user, subject=subject, branch=branch, text=text)
        return HttpResponse("")
    else:
        if (item == "SendText"):
            return render(request, 'index/commentpage.html')
        elif (item == "rating"):
            return render(request, 'index/404.html')
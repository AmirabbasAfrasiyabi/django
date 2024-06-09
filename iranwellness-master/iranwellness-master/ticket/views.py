from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from ticket.models import *
from services.models import serviceModel


@login_required(redirect_field_name='', login_url='/login/')
def ticket_list(request):
    user = request.user
    if request.method == 'POST':
        tickets = TicketOnServices.objects.filter(user=user)
        return render(request, 'ticket/ajax_search.html', {'tickets':tickets})
    tickets = TicketOnServices.objects.filter(user= user)
    return render(request, 'ticket/ticketlist.html', {'tickets':tickets})

@login_required(redirect_field_name='', login_url='/login/')
def NewTicket(request):
    if request.method == 'POST':
        service      = serviceModel.objects.get(name = request.POST['service'])
        topic        = request.POST['topic']
        message      = request.POST['message']
        ticket       = TicketOnServices.objects.create(user=request.user, service=service, topic=topic)
        content_type = ContentType.objects.get_for_model(TicketOnServices)
        image        = request.FILES.get('picture', False)
        newChat = Chat.objects.create(user=request.user, message=message, content_type=content_type, object_id=ticket.id)
        if (image):
            newChat.image = image
            newChat.save()
        return HttpResponse("")
    services = serviceModel.objects.all()
    return render(request, 'ticket/NewTicket.html', {'services':services})

@login_required(redirect_field_name='', login_url='/login/')
def ticket_detail(request, id):
    if request.method == 'POST':
        message      = request.POST['message']
        content_type = ContentType.objects.get_for_model(TicketOnServices)
        image        = request.FILES.get('picture', False)
        newchat = Chat.objects.create(user=request.user, message=message, content_type=content_type, object_id=id) 
        if (image):
            newChatTicket.image = image
            newChatTicket.save()        
        return HttpResponse("")
    ticket = TicketOnServices.objects.get(id=id)
    return render(request, 'ticket/ticketdetail.html', {'ticket':ticket})

@login_required(redirect_field_name='', login_url='/login/')
def closeticket(request, id):
    ticket = TicketOnServices.objects.get(id=id)
    ticket.status= "closed"
    ticket.save()
    return HttpResponse("")

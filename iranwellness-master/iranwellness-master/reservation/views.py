from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from persiantools.jdatetime import JalaliDateTime, JalaliDate
from services.models import serviceModel
from reservation.models import *
from reservation.functions import *
from authapp.models import *
import jdatetime


# --------------params--------------
shift = 2  # reservation starts for 2 days from now
number_of_days_to_show = 90
visitstart = 8  # start visit at 8:00
visitend = 17  # start visit at 17:00
duration = 30  # minutes visit
# ----------------------------------

@login_required(login_url='/login/')
def services(request):
    services = serviceModel.objects.all()
    return render(request, 'reservation/listservices.html', {'services':services})

def serviceoptions(request, slug):
    print(slug)
    template_name = 'reservation/serviceoptions.html'
    service = serviceModel.objects.get(slug=slug)
    context = {'service':service}
    return render(request, template_name, context)

@login_required(redirect_field_name='', login_url='/login/')
def daychoose(request):
    today = JalaliDate.today()
    firstvalidday= today + timedelta(days=shift)
    month = firstvalidday.month
    year  = firstvalidday.year
    return render(request, 'reservation/day_choose.html', {'month': month, 'year': year})
    

@login_required(redirect_field_name='', login_url='/login/')
def timechoose(request, year, month, day):
    device=request.path.split('/')[3]

    if device=='queueHealth':
        fee1='1000'
        fee2='2000'
        fee3='2500'
    elif device=="queueResonance":
        fee1='2000'
        fee2='3000'
        fee3='3500'
    return render(request, 'reservation/timechoose.html',{'fee1': fee1,
                                                          'fee2': fee2,
                                                          'fee3': fee3})

######################
totalvisits = 18
######################
def monthinfo(request, idx):
    firstnext = JalaliDate.today()+timedelta(shift)
    month = firstnext.month
    year  = firstnext.year
    x = month + idx
    if (x > 12):
        month = x - 12
        year = year + 1
    else:
        month = month +idx
    dayiter = JalaliDate(year, month, 1)
    URLbeforeDate=request.GET.get('URLbeforeDate')
    if dayiter.month == firstnext.month:
        dayiter = firstnext

    f = '<div class="d-flex justify-content-center mt-2">'
    i = dayiter.day
    for j in range(dayiter.weekday()):
        f = f+'<a class="weekdays"></a>'
    while dayiter.month == month:
        if dayoff.objects.filter(year=year, month=month, day=i).exists():
            f = f+'<a class="weekdays day-off">'+str(i)+'</a>'
        else:
            f = f+"<a class=\"weekdays\" href=\""+URLbeforeDate+str(year)+"/"+str(month)+"/"+str(i)+"\">"+str(i)+"</a>"
        if dayiter.weekday() == 6:
            f = f+'</div><div class="d-flex justify-content-center mt-2">'
        dayiter = dayiter+timedelta(days=1)
        i = i+1
    for j in range(7-dayiter.weekday()):
        f = f+'<a class="weekdays"></a>'
    f = f+'</div>'
    return HttpResponse(f)


@login_required(redirect_field_name='', login_url='/login/')
def search(request, year, month, day, duration):
    device=request.path.split('/')[3]
    if device=='queueHealth':
        database=healthreservation
    elif device=="queueResonance":
      database=resonancereservation  
    else:
        return HttpResponse(status(400))

    if dayoff.objects.filter(year=year, month=month, day=day).exists():
        return HttpResponse("امکان ویزیت در روز انتخابی وجود ندارد.")
    base = visit(year=year, month=month, day=day, hour=8)
    text = ""
    for i in range(totalvisits-duration+1):
        flag = False
        for c in range(duration):
            if database.objects.filter(year=year, month=month, day=day,order=(i+1+c)).exists():
                flag = True
                break
        if flag == False:
            start = base+timedelta(minutes=(30*i))
            end   = start+timedelta(minutes=(30*duration))
            text += "<option value=\""+str(duration)+"/"+str(
                i+1)+"\">" + start.strftime("%H:%M - ")+end.strftime("%H:%M") + "</option>"
    if text != "":
        text = "<select id=\"order\" class=\"form-control\">"+text+"</select>"
        text += "<button class=\"normal-button\" onclick=\"display()\">ثبت</button>"
        return HttpResponse(text)
    else:
        return HttpResponse("نوبتی یافت نشد.")

@login_required(redirect_field_name='', login_url='/login/')
def result(request, year, month, day, duration, order):
    user=request.user
    ## reservation date time
    VisitDate=JalaliDateTime(year=year, month=month, day=day).strftime('%Y/%m/%d')
    ## start time
    if  (order%2 == 0):
        Shour=int(8 + (0.5*(order-2)))
        Sminute=30
    elif (order%2 == 1):
        Shour=int(8 + (0.5*(order-1)))
        Sminute=0
    ## end time
    if (duration== 1):
        if (order%2 == 0):
            Ehour=Shour+1
            Eminute=0
        elif (order%2 == 1):
            Ehour=Shour
            Eminute=30
    elif (duration== 2):
        Ehour=Shour+1
        Eminute=Sminute
    elif (duration== 3):
        if (order%2 == 0):
            Eminute=0
            Ehour=Shour+2
        elif (order%2 == 1):
            Eminute=30
            Ehour=Shour+1
    ## price
    device=request.path.split('/')[3]
    if device=='queueHealth':
        Type= "ارزیابی"
        if (duration== 1):
            Amount= 1000
        elif (duration== 2):
            Amount= 2000
        elif (duration== 3):
            Amount= 2500
    elif (device=="queueResonance"):
        Type= "ارتقاء"
        if (duration== 1):
            Amount= 2000
        elif (duration== 2):
            Amount= 3000
        elif (duration== 3):
            Amount= 3500
    ST=JalaliDateTime(year=year, month=month, day=day, hour=Shour, minute=Sminute).strftime("- %H:%M")
    ET=JalaliDateTime(year=year, month=month, day=day, hour=Ehour, minute=Eminute).strftime("%H:%M")
    if request.method == 'POST':
       year=int(request.POST.get('Year'))
       month=int(request.POST.get('Month'))
       day=int(request.POST.get('Day'))
       order=int(request.POST.get('Order'))
       device=request.POST.get('Device')
       duration=int(request.POST.get('Duration'))
       if device=='queueHealth':
          database=healthreservation
       elif device=="queueResonance":
          database=resonancereservation
       for x in range(duration):
          if database.objects.filter(year=year, month=month, day=day, order=(x+order)).exists():
            return HttpResponse(status=400)
       base = visit(year=year, month=month, day=day, hour=8)
       start = base+timedelta(minutes=(30*(order-1)))
       end = start+timedelta(minutes=(30*duration))
       string = str("{}/{}/{}  روز {}  ساعت: ").format(year, month, day, weekday[jdatetime.date(year, month, day).weekday()]) + start.strftime("%H:%M-")+end.strftime("%H:%M")
       database.objects.create(user=request.user, year=year, month=month, day=day, order=order ,duration=duration, string=string)
       return render(request, 'reservation/reserveResult.html', {'type'      : Type,
                                                                 'Date'      : VisitDate,
                                                                 'Amount'    : Amount,
                                                                 'STime'     : ST,
                                                                 'ETime'     : ET,
                                                                 'Year'      : year,
                                                                 'Month'     : month,
                                                                 'Day'       : day,
                                                                 'Device'    : device,
                                                                 'Order'     : order,
                                                                 'Duration'  : duration,
                                                                 'message'   : 'رزرو شما با موفقیت انجام شد.'})
    else:
       ## prevoius reservations without payment
       permission="invalid"
       inf1=healthreservation.objects.filter   (user=user, paid=False)
       inf2=resonancereservation.objects.filter(user=user, paid=False)
       if ( (inf2.count() <=1) and (inf1.count()<=1) ):
           permission="valid" 
       return render(request, 'reservation/reserveResult.html', {'permission': permission,
                                                                 'type'      : Type,
                                                                 'Date'      : VisitDate,
                                                                 'Amount'    : Amount,
                                                                 'STime'     : ST,
                                                                 'ETime'     : ET,
                                                                 'Year'      : year,
                                                                 'Month'     : month,
                                                                 'Day'       : day,
                                                                 'Device'    : device,
                                                                 'Order'     : order,
                                                                 'Duration'  : duration})

@login_required(redirect_field_name='', login_url='/login/')    
def resultservices(request, servicetype):
    if (servicetype == "queueHealth"):
        database= healthreservation
    elif (servicetype == "queueResonance"):
        database=resonancereservation 
    if request.method =="POST":
        PK= int(request.POST.get('PK'))
        result=database.objects.get(pk=PK)
        user=User.objects.get(username=result.user.username)
        uinfo=profiledb.objects.get(user=user)
        return render(request, 'reservation/resultservices.html',{'name'  :servicetype,
                                                                  'uinfo' :uinfo,
                                                                  'result':result })
    else:
        info=database.objects.filter(user=request.user, visit= True)
        if (info.count() > 0):
            return render(request, 'reservation/resultservices.html',{'name':servicetype,
                                                                      'info':info })
        else:
            return render(request, 'reservation/resultservices.html',{'name'   :servicetype,
                                                                      'message':'مراجعه‌ای انجام نشده است.' })


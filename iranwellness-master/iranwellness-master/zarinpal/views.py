from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from zeep import Client
from django.shortcuts import render
from reservation.functions import *
from zarinpal.models import *
from manager.models import *
from reservation.models import *
from django.core.exceptions import ObjectDoesNotExist
from persiantools.jdatetime import JalaliDateTime
from django.utils import timezone

#MERCHANT = '36689804-5a86-453d-bcf7-b4b73d5a7429'
#client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

#description = "پرداخت ایران ولنس"  # Required

## Important: need to edit for realy server.
#email='maryam.ahmadinejad9@gmail.com'
#mobile='09120977067'

def send_request(request):
    CallbackURL = 'http://127.0.0.1:8000/verify/'
    if request.method == 'POST':
        year    =int(request.POST.get('Year'))
        month   =int(request.POST.get('Month'))
        day     =int(request.POST.get('Day'))
        order   =int(request.POST.get('Order'))
        device  =request.POST.get('Device')
        duration=int(request.POST.get('Duration'))
        if device=='queueHealth':
           if (duration== 1):
               amount= 1000
           elif (duration== 2):
               amount= 2000
           elif (duration== 3):
               amount= 2500
        elif (device=="queueResonance"):
           if (duration== 1):
               amount= 2000
        elif (duration== 2):
               amount= 3000
        elif (duration== 3):
               amount= 3500
        request.session["year"]   = year
        request.session["month"]  = month
        request.session["day"]    = day
        request.session["order"]  = order
        request.session["device"] = device
        request.session["duration"] = duration
        request.session["amount"] = amount
        result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))

def send_cartRequest(request):
    CallbackURL = 'http://127.0.0.1:8000/cartverify/'
    if (request.method == 'POST'):
        name  =    request.POST.get('name')
        amount=int(request.POST.get('price'))# Toman / Required
        request.session["name"]   =name
        request.session["amount"] = amount
        result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))

def cartverify(request):
    if request.GET.get('Status') == 'OK':
        amount= request.session["amount"]
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            name=request.session["name"]
            receipt= ShoppingReceipt.objects.get(user=request.user , name=name, price=amount)
            receipt.paid=True
            receipt.save()
            del request.session["amount"]
            del request.session["name"]
            return render(request, 'zarinpal/paymentstatus.html',  {'message': 'تراکنش با موفقیت صورت پذیرفت.\nکد رهگیری:',
                                                                    'code'   : str(result.RefID),
                                                                    'St'     : "Cart"})
        elif result.Status == 101:
            return render(request, 'zarinpal/paymentstatus.html',  {'message': 'تراکنش  قبلا تایید شده است!',
                                                                    'St'     : "Cart"})
        else:
            return render(request, 'zarinpal/paymentstatus.html',  {'message': 'تراکنش انجام نپذیرفت.',
                                                                    'St'     : "Cart"})
    else:
        return render(request, 'zarinpal/paymentstatus.html',  {'message': 'تراکنش انجام نپذیرفت.',
                                                                    'St' : "Cart"})

def verify(request):
    if request.GET.get('Status') == 'OK':
        amount= request.session["amount"]
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:  
            year=  request.session["year"]
            month= request.session["month"]
            day=   request.session["day"]
            order= request.session["order"]
            duration=request.session["duration"]
            device=request.session["device"]
            if device=='queueHealth':
                database=healthreservation
            elif device=="queueResonance":
                database=resonancereservation
            try:
                rec=database.objects.get(user=request.user, year=year, month=month, day=day, order=order, duration=duration)
            except ObjectDoesNotExist:
                for x in range(duration):
                    if database.objects.filter(year=year, month=month, day=day, order=(x+order)).exists():
                        return HttpResponse(status=400)
                base = visit(year=year, month=month, day=day, hour=8)
                start = base+timedelta(minutes=(30*(order-1)))
                end = start+timedelta(minutes=(30*duration))
                string = str("{}/{}/{}  روز {}  ساعت: ").format(year, month, day, weekday[time(year, month, day).weekday()]) + start.strftime("%H:%M-")+end.strftime("%H:%M")
                for x in range(duration):
                      database.objects.create(user=request.user, year=year, month=month, day=day, order=order+x, duration=duration, string=string)
            rec=database.objects.get(user=request.user, year=year, month=month, day=day, order=order, duration=duration)
            rec.paid=True
            rec.time_paied=timezone.now()
            rec.save()
            del request.session["year"]
            del request.session["month"]
            del request.session["day"]
            del request.session["order"]
            del request.session["duration"]
            del request.session["device"]
            del request.session["amount"]
            return render(request, 'zarinpal/paymentstatus.html',  {'message': 'تراکنش با موفقیت صورت پذیرفت.\nکد رهگیری:',
                                                                    'code'   : str(result.RefID),
                                                                    'St'     : "Normal"})
        elif result.Status == 101:
            return render(request, 'zarinpal/paymentstatus.html',  {'message': 'تراکنش  قبلا تایید شده است!',
                                                                    'St'     : "Normal"})
        else:
            return render(request, 'zarinpal/paymentstatus.html',  {'message': 'تراکنش انجام نپذیرفت.',
                                                                    'St'     : "Normal"})
    else:
            return render(request, 'zarinpal/paymentstatus.html',  {'message': 'تراکنش انجام نپذیرفت.',
                                                                    'St'     : "Normal"})
@login_required(redirect_field_name='', login_url='/login/')
def payments(request):
    user=request.user
    HealthInfo=healthreservation.objects.filter(user=user, visit= False)
    ResonanceInfo=resonancereservation.objects.filter(user=user, visit= False)
    QuickInfo=quickreceipt.objects.filter(phone=user.username)
    ShoppingInfo=ShoppingReceipt.objects.filter(user=user, paid=False)
    if request.method == 'POST':
        determiner=request.POST.get('determiner')
        if (determiner == "shop"):
            name =    request.POST.get('name')
            price=int(request.POST.get('price'))
            ShoppingReceipt.objects.get(user=user, name=name, price=price).delete()
            ShoppingInfo=ShoppingReceipt.objects.filter(user=user, paid=False)
            return render(request, 'zarinpal/payments.html', {'ResonanceInfo': ResonanceInfo,
                                                              'HealthInfo'   : HealthInfo,
                                                              'QuickInfo'    : QuickInfo,
                                                              'ShoppingInfo' : ShoppingInfo})
        elif (determiner == "service"):
            year    = int(request.POST.get('Year'))
            month   = int(request.POST.get('Month'))
            day     = int(request.POST.get('Day'))
            order   = int(request.POST.get('Order'))
            device  = request.POST.get('Device')
            duration= int(request.POST.get('Duration'))
            if device=='queueHealth':
                     database=healthreservation
            elif device=="queueResonance":
                     database=resonancereservation
            database.objects.get(user=request.user, year=year, month=month, day=day, order=order, duration=duration).delete()
            HealthInfo=healthreservation.objects.filter(user=user, visit= False)
            ResonanceInfo=resonancereservation.objects.filter(user=user, visit= False)
            if (len(ResonanceInfo) == 0 and len(HealthInfo) == 0):
                return render(request, 'zarinpal/payments.html', {'message'     : 'در بخش پشتیبانی حضوری برای شما هیچگونه رزروی ثبت نشده است.',
                                                                  'QuickInfo'   : QuickInfo,
                                                                  'ShoppingInfo': ShoppingInfo})
            else:
                return render(request, 'zarinpal/payments.html', {'ResonanceInfo': ResonanceInfo,
                                                                  'HealthInfo'   : HealthInfo,
                                                                  'QuickInfo'    : QuickInfo,
                                                                  'ShoppingInfo' : ShoppingInfo})
    else:
        ShoppingInfo=ShoppingReceipt.objects.filter(user=user, paid=False)
        if (len(ResonanceInfo) == 0 and len(HealthInfo) == 0):
           return render(request, 'zarinpal/payments.html', {'message'     : 'در بخش پشتیبانی حضوری برای شما هیچگونه رزروی ثبت نشده است.',
                                                             'QuickInfo'   : QuickInfo,
                                                             'ShoppingInfo': ShoppingInfo})
        else:
           return render(request, 'zarinpal/payments.html', {'ResonanceInfo': ResonanceInfo,
                                                             'HealthInfo'   : HealthInfo,
                                                             'QuickInfo'    : QuickInfo,
                                                             'ShoppingInfo' : ShoppingInfo})
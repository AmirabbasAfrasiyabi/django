from django.shortcuts import render,redirect
from authapp.models import sms_verification_table
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from persiantools.digits import fa_to_en
from django.http import HttpResponse, HttpResponseRedirect
from random import randint
from kavenegar import *
from authapp.models import *
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import date


def OTP(phone):
    key = str(randint(1000, 9999))
    try:
        api = KavenegarAPI('3146536276686E456A764345486F73592B75787266746273464C507377756166')
        params = {
            'receptor': phone,
            'template': 'verify',
            'token': key,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(str(e))
    except HTTPException as e:
        print(str(e))
    return key
    

def phoneverification(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if (len(phone)>0):
            try:
                p=sms_verification_table.objects.get(phone_number=phone)
                request.session["phone_number"] = p.phone_number
                key=OTP(phone)
                p.key=key
                p.save()
                return HttpResponseRedirect('/activation/')
            except ObjectDoesNotExist:
                sms_verification_table.objects.create(phone_number=phone)
                info=sms_verification_table.objects.get(phone_number=phone)
                request.session["phone_number"] = info.phone_number
                key=OTP(phone)
                info.key=key
                info.save()
                return HttpResponseRedirect('/activation/')   
        else:
            return render(request, 'authapp/phoneverification.html')
    else:
        return render(request, 'authapp/phoneverification.html')

def activation(request):
    if request.method == 'POST':
        phone = request.session["phone_number"]
        try:
            k=sms_verification_table.objects.get(phone_number=phone, key= request.POST.get('key'))
            if (request.POST.get('password') == request.POST.get('repass')):
                del request.session["phone_number"]
                u, created = User.objects.get_or_create(username=k.phone_number)
                u.set_password(request.POST.get('password'))
                u.save()
                if (not u.groups.all()):
                    user_group = Group.objects.get(name="OrdineryUser")
                    u.groups.add(user_group)
                auth.login(request, u)
                return HttpResponseRedirect('/dashboard/')
            elif (request.POST.get('password') != request.POST.get('repass')):
                return render(request, 'authapp/activation.html',{'error': 'رمز عبور و تکرار رمز عبور برابر نیستند!'})
        except ObjectDoesNotExist:
            return render(request, 'authapp/activation.html',{'error': 'کد فعال‌سازی واردشده صحیح نمی‌باشد!'})
    else:
        return render(request, 'authapp/activation.html')

@login_required(redirect_field_name='', login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == "POST":
        try:
            u = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            auth.login(request, u)
            user=request.user
            if (user.is_staff == False):
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponseRedirect('/MSlogin/')
        except:
            return render(request, 'authapp/login.html', {"error": "رمز عبور یا شماره همراه واردشده صحیح نمی‌باشد!"})
    return render(request, 'authapp/login.html')


@login_required(redirect_field_name='/profile/', login_url='/login/')
def profile(request):
    if request.method == 'POST':
        obj, created = profiledb.objects.update_or_create(user=request.user, defaults={
            "firstname": request.POST.get('firstname'),
            "lastname" : request.POST.get('lastname'),
            "Email"    : request.POST.get('email'),
            "job"      : request.POST.get('job'),
            "phone1"   : fa_to_en(request.POST.get('phone1')),
            "address1" : request.POST.get('address1'),
            "address2" : request.POST.get('address2'),
            "phone3"   : fa_to_en(request.POST.get('phone3'))
        })
        user = User.objects.get (username=request.user.username)
        user.first_name = request.POST.get('firstname')
        user.last_name  = request.POST.get('lastname')
        user.email      = request.POST.get('email')
        user.save()

        try:
            image=request.FILES['picture']
            profile_instance=profiledb.objects.get(user=request.user)
            profile_instance.image=image
            profile_instance.save()
        except:
            profile_instance = profiledb.objects.get(user=request.user)
        if (not request.user.groups.all()):
            user_group = Group.objects.get(name="OrdineryUser")
            request.user.groups.add(user_group)
        ## check wellid
        profile_instance = profiledb.objects.get(user=request.user)
        if (not profile_instance.wellid):
            today = date.today()
            year = today.year
            stryear = str(year)[2:]
            month = today.month
            if (month<10):
                strmonth = "0" + str(month)
            else:
                strmonth = str(month)
            day =today.day
            if (day<10):
                strday = "0" + str(day)
            else:
                strday = str(day)
            FPwellid = stryear + strmonth + strday
            if (profiledb.objects.filter(wellid__startswith= FPwellid).exists()):
                for n in range(1,1000):
                    if (n<10):
                        ID = FPwellid + "00" + str(n)
                    elif (n>9 and n<100):
                        ID = FPwellid + "0"  + str(n)
                    else:
                        ID = FPwellid + str(n)
                    if (profiledb.objects.filter(wellid = ID).exists()):
                        continue
                    else:
                        profile_instance.wellid = ID
                        break
            else:
                profile_instance.wellid = FPwellid + "001"
            profile_instance.save()    
        if (request.POST.get('winpath')):
            windowpath = request.POST.get('winpath')
            return redirect(windowpath)
        else:
            return render(request, 'authapp/profile.html', {"data": profile_instance,
                                                            "message": "showModal"
                                                            })
    else:
        try:
            profile_instance = profiledb.objects.get(user=request.user)
            return render(request, 'authapp/profile.html', {"data": profile_instance})
        except:
            return render(request, 'authapp/profile.html')
            
@login_required(redirect_field_name='', login_url='/login/')
def membership(request):
    user=request.user
    membershipType = ''
    try:
        info = profiledb.objects.get(user=user)
        if   (info.membershipType == 'Normal') : membershipType = 'عادی'
        elif (info.membershipType == 'Silver') : membershipType = 'نقره‌ای'
        elif (info.membershipType == 'Bronze') : membershipType = 'برنزی'
        elif (info.membershipType == 'Golden') : membershipType = 'طلایی'
        elif (info.membershipType == 'Diamond'): membershipType = 'الماسی'
        status= "valid"
    except ObjectDoesNotExist:
        status= "invalid"
    return render(request, 'authapp/membership.html',{'membershipType': membershipType,
                                                      'status'        : status
                                                     })

@login_required(redirect_field_name='', login_url='/login/')
def PlanType(request, planType):
    return render(request, 'authapp/membershipPlans/'+ planType + '.html')

def testValidation(request):
    return render(request, 'authapp/test.html')
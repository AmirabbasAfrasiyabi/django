from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
##
from django.utils import timezone
from datetime import timedelta
from persiantools.jdatetime import JalaliDateTime, JalaliDate
##
from specialists.mixins import *
from reservation.functions import *
from django.contrib.auth.models import User
from authapp.models import *
from reservation.models import *
from ticket.models import *
from quiz.models import *
from manager.models import quickreceipt


@login_required(redirect_field_name='', login_url='/login/')
def MSlogin(request):
    return render(request, 'manager/MSlogin.html')


class ManagerDashboard(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, TemplateView):
    group_required = [u'manager']
    template_name = 'manager/managerDashboard.html'


#####################################################################################################################
############      USERS
#####################################################################################################################
class UsersListView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, ListView):
    group_required = [u'manager']
    template_name = 'manager/user/users_list.html'
    context_object_name = 'users_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all()
        ##
        wellness_id = self.request.GET.get('code','')
        firstname   = self.request.GET.get('firstname','')
        lastname    = self.request.GET.get('lastname','')
        phonenumber = self.request.GET.get('phone','')
        ##
        if wellness_id:
            queryset = queryset.filter(profiledb__wellid__iexact=wellness_id)
        if firstname:
            queryset = queryset.filter(profiledb__firstname__icontains=firstname)
        if lastname:
            queryset = queryset.filter(profiledb__lastname__icontains=lastname)
        if phonenumber:
            queryset = queryset.filter(username__icontains=phonenumber)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        QUERY_STRING = self.request.GET.copy()
        if 'page' in QUERY_STRING:
            del QUERY_STRING['page']
        QUERY_STRING = QUERY_STRING.urlencode()
        context['QUERY_STRING']  = QUERY_STRING
        return context


class UserDetailView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']
    template_name = 'manager/user/user_detail.html'
    
    def get(self, request, id):
        user = User.objects.get(id=id) 
        context = {'user' : user}
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        username =  request.POST.get('username')
        wellid =    request.POST.get('wellid', "")
        firstname = request.POST.get('firstname', "")
        lastname =  request.POST.get('lastname', "")
        Email =     request.POST.get('Email', "")
        phone1 =    request.POST.get('phone1', "")
        job =       request.POST.get('job', "")
        phone3 =    request.POST.get('phone3', "")
        address1 =  request.POST.get('address1', "")
        address2 =  request.POST.get('address2', "")
        isActive =  request.POST.get('isActive', False)
        
        ## check required-inputs
        if(firstname == "" or lastname == "" ):
            response = JsonResponse({'status':'fail','message':"یک یا چند عدد از فیلد های الزامی خالی است"})
            return response
        user_object = User.objects.get(id = id)
        
        ## check user existence
        if ( username != user_object.username ):
            if ( User.objects.filter(username = username).exists() ):
                response = JsonResponse({'status':'fail','message':"کاربری با این شماره همراه وجود دارد."})
                return response
        user_object.username=username
        user_object.save()

        ## update or create profile
        profiledb_object, created = profiledb.objects.update_or_create (
            user = user_object,
            defaults = { "wellid"   : wellid,
                         "firstname": firstname,
                         "lastname" : lastname,
                         "Email"    : Email,
                         "address1" : address1,
                         "address2" : address2,
                         "phone1"   : phone1,
                         "job"      : job,
                         "phone3"   : phone3,
                         "isActive" : isActive
                       }
            )
        return JsonResponse({'status':'success','message':"اطلاعات کاربر با موفقیت اصلاح شد."})


class AddUserView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']
    template_name = 'manager/user/add_user.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return JsonResponse({'status':'success'})
#####################################################################################################################



#####################################################################################################################
############      RESERVATION
#####################################################################################################################
# --------------params--------------
shift = 0  # reservation starts for 0 days from now
number_of_days_to_show = 90
visitstart = 8  # start visit at 8:00
visitend = 17  # start visit at 17:00
duration = 30  # minutes visit
totalvisits = 18
# ----------------------------------


class UpdateCalendar(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']
    template_name = 'manager/reservation/updatecalendar.html'
    today = JalaliDate.today()

    def get(self, request):
        year=self.today.year
        extract_time_ir(year)
        extract_time_ir(year+1)
        extract_weekends()
        calendar = dayoff.objects.all().order_by('year','month','day')
        years = [self.today.year, self.today.year+1]
        return render(request, self.template_name, {'calendar': calendar, 'days': days, 'months': months, 'years': years})

    def post(self, request):
        day = int(request.POST.get('dayselect'))
        month = int(request.POST.get('monthselect'))
        year = int(request.POST.get('yearselect'))+self.today.year
        if dayoff.objects.filter(year=year, month=month, day=day).exists():
            dayoff.objects.filter(year=year, month=month, day=day).delete()
        else:
            dayoff.objects.create(year=year, month=month, day=day)
        years = [self.today.year, self.today.year+1]
        calendar = dayoff.objects.all().order_by('year','month','day')
        return render(request, self.template_name, {'calendar': calendar, 'days': days, 'months': months, 'years': years})


class MonthinfoManager(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']

    def get(self, request, idx):
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
                numberOfReserves = healthreservation.objects.filter(year=year,month=month,day=i).count()+resonancereservation.objects.filter(year=year,month=month,day=i).count()
                if (numberOfReserves > 0):
                    f = f+"<a class=\"weekdays\" href=\""+URLbeforeDate+str(year)+"/"+str(month)+"/"+str(i)+"\">"+str(i)+"<div class=\"weekdays-reserved-identifier\"></div></a>"
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


class ReservationOption(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, TemplateView):
    group_required = [u'manager']
    template_name = 'manager/reservation/reservationOptions.html'


class ListView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']

    def get(self, request, year, month, day):
        class mylist:
            def __init__(self,code,firstname,lastname,phonenumber,string,device,device2,paid,visit,pk,order):
                self.code       = code
                self.firstname  = firstname
                self.lastname   = lastname
                self.phonenumber= phonenumber
                self.string     = string
                self.device     = device
                self.device2    = device2
                self.paid       = paid
                self.visit      = visit
                self.pk         = pk
                self.order      = order

        items=[]
        s=''
        for item in healthreservation.objects.filter(year=year, month=month, day=day).order_by('order'):
            if s != item.string:
                s=item.string
                try:
                    profile = profiledb.objects.get(user=item.user)
                    wellid = profile.wellid
                    firstname = profile.firstname
                    lastname = profile.lastname
                except:
                    wellid = ''
                    firstname = ''
                    lastname = ''
                items.append(mylist(wellid,
                                    firstname,
                                    lastname,
                                    item.user.username,
                                    item.string,
                                    'هلث',
                                    'health',
                                    item.paid,
                                    item.visit,
                                    item.pk,
                                    item.order))
        s=''
        for item in resonancereservation.objects.filter(year=year, month=month, day=day).order_by('order'):
            if s != item.string:
                s=item.string
                try:
                    profile = profiledb.objects.get(user=item.user)
                    wellid = profile.wellid
                    firstname = profile.firstname
                    lastname = profile.lastname
                except:
                    wellid = ''
                    firstname = ''
                    lastname = ''
                items.append(mylist(wellid,
                                    firstname,
                                    lastname,
                                    item.user.username,
                                    item.string,
                                    'رزونانس',
                                    'resonance',
                                    item.paid,
                                    item.visit,
                                    item.pk,
                                    item.order))
        return render(request, 'manager/list-view.html',{'items':items,
                                                     'year' :year,
                                                     'month':month,
                                                     'day'  :day
        })
    
    def post(self, request, year, month, day):
        username = request.POST['username']
        device   = request.POST['device']
        operation= request.POST['operation']
        if (device == "health"):
            info= healthreservation.objects.get (user=User.objects.get(username=username), year=year, month=month, day=day)
        elif (device == "resonance"):
            info= resonancereservation.objects.get (user=User.objects.get(username=username), year=year, month=month, day=day)
        if (operation == "pay"):
            info.paid= True
            info.time_paied = timezone.now()
            info.save()
        elif (operation == "visit"):
            info.visit= True
            info.save()
        elif (operation == "cancel"):
            info.delete()
        return HttpResponse("")


class ChooseReservationService(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, TemplateView):
    group_required = [u'manager']
    template_name = 'manager/reservation/chooseService.html'


class ManagerDayChoose(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']
    template_name = 'manager/reservation/day-choose.html'

    def get(self, request, reserveType):
        today = JalaliDate.today()
        year  = today.year
        month = today.month
        print(year)
        if (reserveType == 'searchreserve'):
            T = 'search'
        elif(reserveType == 'newreserve'):
            T = 'new'
        return render(request, self.template_name, {'month': month, 'year': year, 'type': T})


class TimeChooseM(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, TemplateView):
    group_required = [u'manager']
    template_name = 'manager/reservation/timechooseM.html'


class Search(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']

    def get(self, request, year, month, day, duration):
        ## get device
        device=request.path.split('/')[4]
        if device=='queueHealth':
            database=healthreservation
        elif device=="queueResonance":
          database=resonancereservation  
        else:
            return JsonResponse({'status':'fail', 'message':'امکان ویزیت برای دستگاه موردنظر وجود ندارد!'})
        ## check day-off   
        if dayoff.objects.filter(year=year, month=month, day=day).exists():
            return JsonResponse({'status':'fail', 'message':'امکان رزرو در روز انتخابی وجود ندارد!'})
        ## get valid-days
        base = visit(year=year, month=month, day=day, hour=8)
        result=[]
        for i in range(totalvisits-duration+1):
            order = i+1
            flag = False
            for c in range(duration):
                if database.objects.filter(year=year, month=month, day=day,order=(i+1+c)).exists():
                    flag = True
                    break
            if flag == False:
                start = base+timedelta(minutes=(30*i))
                end   = start+timedelta(minutes=(30*duration))
                result.append({'value':f'{duration}/{order}', 'string':f'{start.strftime("%H:%M - ")}{end.strftime("%H:%M")}'})
        ## check result
        if (result):
            return JsonResponse({'status':'success', 'result':result})
        else:
            return JsonResponse({'status':'fail', 'message':'نوبتی یافت نشد!'})


class ResultM(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']
        
    def get(self, request, year, month, day, duration, order):
        ## device
        device=request.path.split('/')[4]
        if device=='queueHealth':
            Type= "عمومی"
        elif (device=="queueResonance"):
            Type= "تخصصی"
        
        ## start time
        visit_date=JalaliDateTime(year=year, month=month, day=day).strftime('%Y/%m/%d')
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
        ST=JalaliDateTime(year=year, month=month, day=day, hour=Shour, minute=Sminute).strftime("%H:%M")
        ET=JalaliDateTime(year=year, month=month, day=day, hour=Ehour, minute=Eminute).strftime("%H:%M")
        
        return render(request, 'manager/reservation/reserveResult-manager.html', {
                                                                                   'type'      : Type,
                                                                                   'date'      : visit_date,
                                                                                   'time'      : f'{ST} - {ET}'
                                                                                 })
    
    def post(self, request, year, month, day, duration, order):

        ##
        posted_data = request.POST
        phonenumber         = posted_data.get('username')
        wellness_id         = posted_data.get('wellid')
        firstname           = posted_data.get('firstname')
        lastname            = posted_data.get('lastname')
        email               = posted_data.get('Email')
        telephone_number    = posted_data.get('phone1')
        social_media_number = posted_data.get('phone3')
        job                 = posted_data.get('job')
        home_address        = posted_data.get('address1')
        workplace_address   = posted_data.get('address2')

        ##
        required_inputs = [phonenumber, firstname, lastname]
        number_of_empty_equired_inputs = sum(required_input == "" for required_input in required_inputs)
        if ( number_of_empty_equired_inputs > 0 ):
            return JsonResponse({'status':'fail','message':'لطفاً ورودی‌های ضروری را پر کنید.!'})

        ## check user
        user, created = User.objects.get_or_create(username=phonenumber)

        ## get service-db
        device=request.path.split('/')[4]
        if device=='queueHealth':
            database=healthreservation
        elif device=="queueResonance":
            database=resonancereservation
        
        ## check duplicate
        for x in range(duration):
            if database.objects.filter(year=year, month=month, day=day, order=(x+order)).exists():
                return JsonResponse({'status':'fail', 'message':'با عرض پوزش امکان ثبت این رزرو وجود ندارد!'})
        
        ## check user-reservations
        if ( database.objects.filter(user=user, year=year, month=month, day=day).exists() ):
            return JsonResponse({'status':'fail', 'message':'با عرض پوزش امکان رزرو بیش از یک مورد در طول روز برای یک کاربر وجود ندارد!'})
        
        ## create reserve
        base = visit(year=year, month=month, day=day, hour=8)
        start = base+timedelta(minutes=(30*(order-1)))
        end = start+timedelta(minutes=(30*duration))
        string = str("{}/{}/{}  روز {}  ساعت: ").format(year, month, day, weekday[JalaliDate(year, month, day).weekday()]) + start.strftime("%H:%M - ")+end.strftime("%H:%M")
        database.objects.create(user=user, year=year, month=month, day=day, order=order ,duration=duration, string=string)

        ## user-profile
        obj, created = profiledb.objects.update_or_create(user=user, defaults = {
                                                                                 "firstname": firstname,
                                                                                 "lastname" : lastname,
                                                                                 "Email"    : email,
                                                                                 "job"      : job,
                                                                                 "phone1"   : fa_to_en(telephone_number),
                                                                                 "address1" : home_address,
                                                                                 "address2" : workplace_address,
                                                                                 "phone3"   : fa_to_en(social_media_number)
                                                                                })

        return JsonResponse({'status':'success', 'message':'رزرو با موفقیت انجام شد.'})
#####################################################################################################################



#####################################################################################################################
############      QUIZ
#####################################################################################################################
class QuizSearchManager(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']

    def get(self, request):
        return render(request, 'manager/quizsearch.html')

    def post(self, request):
        dimensionNames= ["مسئولیت پذیری در قبال خود و عشق", "تنفس","تغذیه","حس کردن","حرکت", "احساس کردن", "فکر کردن", "بازی کردن و کار کردن", "ارتباط برقرار کردن", "صمیمیت", "یافتن معنا", "ورا رفتن"]
        phnumber   = request.POST['phone']
        quiznumber = request.POST['quiznumber']
        try:
            user= User.objects.get(username = phnumber)
            phnumber   = int(phnumber)
            quiznumber = int(quiznumber)
            if (quiznumber == 13):
                     results= wellnessCircle.objects.get(user=user)
                     if (results):
                          return render(request, 'quizresult.html',{'results'      : results,
                                                                    'dimensionName': 'نتیجه تمامی ابعاد' })
                     else:
                          return render(request, 'quizresult.html',{'dimensionName': 'نتیجه تمامی ابعاد',
                                                                    'message'      : 'نتیجه‌ای برای نمایش وجود ندارد.' })
            else:
                results= submit.objects.filter(user=user, number=quiznumber).order_by('-date')
                if (results.count() > 0):
                     return render(request, 'quizresult.html',{'results'      : results,
                                                               'dimensionName': dimensionNames[quiznumber-1] })
                else:
                     return render(request, 'quizresult.html',{'dimensionName': dimensionNames[quiznumber-1],
                                                               'message'      : 'نتیجه‌ای برای نمایش وجود ندارد.' })
        except ObjectDoesNotExist:
               quiznumber = int(quiznumber)
               return render(request, 'quizresult.html',{'dimensionName': dimensionNames[quiznumber-1],
                                                          'message'     : 'چنین کاربری در سیستم ثبت نشده است.' })
#####################################################################################################################



#####################################################################################################################
############      TICKETS
#####################################################################################################################
class Tickets(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']
    template_name = 'manager/ticket/ticketIndex.html'

    def get(self, request):
        tickets= TicketOnServices.objects.all()
        return render(request, self.template_name, {'chats':tickets})

class DetailTicket(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']
    template_name = 'manager/ticket/detail-ticket.html'

    def get(self, request, id):
        ticket = TicketOnServices.objects.get(id=id)
        return render(request, self.template_name, {'ticket':ticket})
#####################################################################################################################



#####################################################################################################################
############      RECEIPT
#####################################################################################################################
class Receipt(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'manager']
    template_name = 'manager/receipt.html'

    def get(self, request):
        lastinfo=quickreceipt.objects.order_by('-time_created')[:4]
        return render(request, self.template_name, {'lastinfo':lastinfo})

    def post(self, request):
        if (request.POST['determiner'] == "1"):
            firstname =request.POST['firstname']
            lastname  =request.POST['lastname']
            phone     =request.POST['phone']
            Number=request.POST['NOReciepts']
            if (firstname and lastname and phone):
                info=quickreceipt.objects.filter(firstname__contains=firstname, lastname__contains=lastname, phone__exact=phone)
                info=info.order_by('-time_created')[:int(Number)]
            elif (firstname and lastname):
                info=quickreceipt.objects.filter(firstname__contains=firstname, lastname__contains=lastname)
                info=info.order_by('-time_created')[:int(Number)]
            elif (firstname and phone):
                info=quickreceipt.objects.filter(firstname__contains=firstname, phone__exact=phone)
                info=info.order_by('-time_created')[:int(Number)]
            elif (lastname and phone):
                info=quickreceipt.objects.filter(lastname__contains=lastname, phone__exact=phone)
                info=info.order_by('-time_created')[:int(Number)]
            elif (firstname):
                info=quickreceipt.objects.filter(firstname__contains=firstname)
                info=info.order_by('-time_created')[:int(Number)]
            elif (lastname):
                info=quickreceipt.objects.filter(lastname__contains=lastname)
                info=info.order_by('-time_created')[:int(Number)]
            elif (phone):
                info=quickreceipt.objects.filter(phone__exact=phone)
                info=info.order_by('-time_created')[:int(Number)]
            else:
                info=quickreceipt.objects.order_by('-time_created')[:int(Number)]   
            
            return render(request, self.template_name, {'lastinfo':info})
        elif (request.POST['determiner'] == "0"):
            fname=request.POST['firstname']
            quickreceipt.objects.create(firstname=request.POST['firstname'], lastname=request.POST['lastname'], title=request.POST['title'], fee=request.POST['fee'], phone=request.POST['phone'], explane=request.POST['explane'])
            lastinfo=quickreceipt.objects.order_by('-time_created')[:4]
            return render(request, self.template_name,  {
                                                          'notification': "Register",
                                                          'lastinfo':lastinfo
                                                        })
        else:
            firstname =request.POST['firstname2']
            lastname  =request.POST['lastname2']
            title     =request.POST['title2']
            fee       =request.POST['fee2']
            phone     =request.POST['phone2']
            explane   =request.POST['explane2']
            BYear     =request.POST['YearBooked']
            BMonth    =request.POST['MonthBooked']
            BDay      =request.POST['DayBooked']
            BHour     =request.POST['HourBooked']
            BMinute   =request.POST['MinuteBooked']
            BSecond   =request.POST['SecondBooked']
            determiner=request.POST['determiner']
            selected=quickreceipt.objects.filter(firstname__exact=firstname, lastname__exact=lastname, title__exact=title, fee__exact=fee, phone__exact=phone, explane__exact=explane)
            for S in selected:
               if (S.time_created.year == BYear , S.time_created.month == BMonth , S.time_created.day == BDay , S.time_created.hour== BHour , S.time_created.minute == BMinute, S.time_created == BSecond):
                  if (determiner   =="2"):
                      S.delete()
                      return HttpResponseRedirect('/receipt/')
                  elif (determiner =="3"):
                      S.time_paied=timezone.now()
                      S.save()
                      return HttpResponseRedirect('/receipt/')
################################################################################################


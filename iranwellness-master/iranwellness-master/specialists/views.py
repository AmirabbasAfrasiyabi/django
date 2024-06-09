from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from persiantools.jdatetime import JalaliDate
##
from django.contrib.auth.models import User
from authapp.models import *
from services.models import serviceModel
from reservation.models import *
from quiz.models import *
from ticket.models import *

from reservation.functions import *
from .mixins import *


class SpecialistsDashboard(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, TemplateView):
    group_required = [u'EDS', u'Health']
    template_name = 'specialists/specialists_dashboard.html'


#####################################################################################
##################################      USERS      ##################################
#####################################################################################
class UsersListView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, ListView):
    group_required = [u'EDS', u'Health']
    template_name = 'specialists/users/users_list.html'
    context_object_name = 'users_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all()
        ##
        firstname   = self.request.GET.get('firstname','')
        lastname    = self.request.GET.get('lastname','')
        phonenumber = self.request.GET.get('phonenumber','')
        ##
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


class UsersDetailView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, DetailView):
    group_required = [u'EDS', u'Health']
    template_name = 'specialists/users/user_detail.html'
    model = User
    pk_url_kwarg = 'id'
    context_object_name = 'user'


###########################################################################################
##################################      RESERVATION      ##################################
###########################################################################################
class ServicesListView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, TemplateView):
    group_required = [u'EDS', u'Health']
    template_name = 'specialists/reservation/services_list.html'


class ReservationDayChooseView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, TemplateView):
    group_required = [u'EDS', u'Health']
    template_name = 'specialists/reservation/day_choose.html'

    def get_context_data(self, **kwargs):
        context = super(ReservationDayChooseView, self).get_context_data(**kwargs)
        context['month'] = JalaliDate.today().month
        context['year']  = JalaliDate.today().year
        return context


class ReservsListView(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, ListView):
    group_required = [u'EDS', u'Health']
    template_name = 'specialists/reservation/reserves_list.html'
    context_object_name = 'reserves_list'

    def get_queryset(self):
        url_parameters = self.kwargs
        ##
        service = url_parameters['service']
        year    = url_parameters['year']
        month   = url_parameters['month']
        day     = url_parameters['day']
        ##
        if (service == 'queueHealth'):
            queryset = healthreservation.objects.filter(year=year, month=month, day=day)
        elif ( service == 'queueResonance'):
            queryset = resonancereservation.objects.filter(year=year, month=month, day=day)
        return queryset


##############################################################
####    Tickets     ##########################################
##############################################################
class specialists_chooseServiceTickets(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'EDS', u'Health']
    template_name = 'specialists/ticket/chooseService.html'
    services = serviceModel.objects.all()
    context = {'services':services}
    def get(self, request):
        return render(request, self.template_name, self.context)

class specialist_list_tickets(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'EDS', u'Health']
    template_name  = 'specialists/ticket/ticketIndex.html'
    def get(self, request, serviceSlug):
        service     = serviceModel.objects.get(slug=serviceSlug)
        serviceName = service.name
        tickets     = TicketOnServices.objects.filter(status = 'open', service=service)
        context = {'serviceName':serviceName, 'tickets':tickets}
        return render(request, self.template_name, context)
      
class specialist_detail_ticket(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u'EDS', u'Health']
    template_name = 'specialists/ticket/ticket-detail.html'
    def get(self, request, serviceSlug, id):
        ## show selected-ticket detail
        ticket = TicketOnServices.objects.get(id=id)
        return render(request, self.template_name, {'ticket':ticket})
    def post(self, request, serviceSlug, id):
        ticket = TicketOnServices.objects.get(id=id)
        ## get form-data and create new-chat for selected ticket
        message       = request.POST['message']
        image         = request.FILES.get('picture', False)
        content_type  = ContentType.objects.get_for_model(ticket)
        newChatTicket = Chat.objects.create(user=request.user, message=message, content_type=content_type, object_id=id)
        if (image):
            newChatTicket.image = image
            newChatTicket.save()
        return redirect('/specialists/tickets/'+ serviceSlug +'/')

##################################################################################################
@login_required(redirect_field_name='', login_url='/login/')
def analysislist(request):
  user=request.user
  if (user.is_staff == False):
        return HttpResponseRedirect('/login/')
  else:
    info      = submit.objects.filter(result="")
    Number1   = info.count()
    info      = wellnessCircle.objects.filter(result="")
    Number2   = info.count()
    Number12  = Number1 + Number2
    Hinfo     = healthreservation.objects.filter(visit=True, result="", result2="", result3="").exclude(duration="1")
    HNumber   = Hinfo.count()
    Rinfo     = resonancereservation.objects.filter(visit=True, result="", result2="", result3="").exclude(duration="1")
    RNumber   = Rinfo.count()
    return render(request, 'specialists/analysis/submitlist.html',{ 'Number12' : Number12,
                                                                    'HNumber'  : HNumber,
                                                                    'RNumber'  : RNumber})
                                                           
@login_required(redirect_field_name='', login_url='/login/')
def analysisoptions(request, name):
  user=request.user
  if (user.is_staff == False):
    return HttpResponseRedirect('/login/')
  else:
    template_name = 'specialists/analysis/analysisOptions.html'
    context = {'type':name}
    return render(request, template_name, context)

@login_required(redirect_field_name='', login_url='/login/')
def quizResultItems(request):
    template_name = 'specialists/analysis/quizresultspecialists-routeslist.html'
    model= submit
    info = model.objects.filter(result="")
    context ={}
    if (info.count()>0):
        x=[]
        Titles = ['عشق و مسئولیت‌پذیری نسبت به خود','تنفس','تغذیه','حس کردن','حرکت','احساس کردن','فکر کردن','بازی کردن و کار کردن','ارتباط برقرار کردن','صمیمیت','یافتن معنا','ورا رفتن']
        for i in range(1, 13):
            Number = info.filter(number=i).count()
            x.append({'title':Titles[i-1] ,'value':Number})
        context = {'info': x}
    return render(request, template_name, context)

@login_required(redirect_field_name='', login_url='/login/')
def quizSubmittedList(request, number):
    template_name = 'specialists/analysis/quizUploadedList.html'
    model = submit
    Titles = ['عشق و مسئولیت‌پذیری نسبت به خود','تنفس','تغذیه','حس کردن','حرکت','احساس کردن','فکر کردن','بازی کردن و کار کردن','ارتباط برقرار کردن','صمیمیت','یافتن معنا','ورا رفتن']
    context = {'title':Titles[number-1]}
    info = model.objects.filter(number=number, result="")
    context.update({'info': info})
    return render(request, template_name, context)

@login_required(redirect_field_name='', login_url='/login/')
def quizsearchSpecialists(request, number, pk):
    template_name  = 'specialists/analysis/quizresultspecialists.html'
    dimensionNames = ["مسئولیت‌پذیری در قبال خود و عشق", "تنفس","تغذیه","حس کردن","حرکت", "احساس کردن", "فکر کردن", "بازی کردن و کار کردن", "ارتباط برقرار کردن", "صمیمیت", "یافتن معنا", "ورا رفتن"]
    dimensionName  = dimensionNames[number-1]
    selected       = submit.objects.get(pk=pk)
    if request.method =="POST":
        result         =     request.POST['result']
        selected.result = result
        try:
            imageresult =request.FILES['picture']
            selected.imageresult=imageresult
        except Exception:
            pass
        try:
            pdfresult   = request.FILES['pdfresult']
            selected.pdfresult = pdfresult
        except Exception:
            pass
        try:
            vresult     = request.FILES['vresult']
            selected.videoresult = vresult
        except Exception:
            pass
        try:
            aresult     = request.FILES['aresult']
            selected.audioresult = aresult
        except Exception:
            pass
        selected.save()
        return render(request, template_name, {'title': dimensionName,
                                               'successmessage'  : 'فایل‌ها با موفقیت ارسال شدند.'})
    else:
        return render(request, template_name, {'info' : selected,
                                               'title': dimensionName })

def uploadfilelist(request, name):
    template_name = 'specialists/analysis/uploadResultList.html'
    firstcontext = {'name':name}
    context = firstcontext.copy()
    database = name.lower()+'reservation'
    info = globals()[database].objects.filter (visit=True, result="", result2="", result3="").exclude(duration="1").order_by('year','month','day','order')
    if (info.count() > 0):
        context.update({'info': info})
    else:
        context.update({'msg': 'مراجعه‌ای برای آپلود فایل وجود ندارد.'})
    return render(request, template_name, context)

class uploadfile(LoginRequiredMixin, GroupOrSuperuserRequiredMixin, View):
    group_required = [u"EDS", u"Health"]
    template_name = 'specialists/analysis/uploadresult.html'
    context = {}
    def get(self, request, name, pk):
        database = name.lower()+'reservation'
        reserve = globals()[database].objects.get(pk=pk)
        self.context = {'reserve' : reserve, 'title': name }
        return render(request, self.template_name, self.context)
    def post(self,request,name,pk):
        ## get reserve database
        self.filterReserve(request,name,pk)
        ## check reserve-results
        self.checkReserveResults(request, name)
        if (self.context):
            return render(request, self.template_name, self.context)
        ## get form data
        self.getformData(request)
        ## check empty uploaded files
        self.checkEmptyUploadedFiles(request,name)
        if (self.context):
            return render(request, self.template_name, self.context)
        ## save files
        self.saveResults(request,name)
        return render(request, self.template_name, self.context)
    def filterReserve(self,request,name,pk):
        database = name.lower()+'reservation'
        self.reserve = globals()[database].objects.get(pk=pk)
    def checkReserveResults(self, request, name):
        if (self.reserve.result or self.reserve.result2 or self.reserve.result3):
            self.context = {'message':'به علت دارا بودن نتیجه قبلی، فایلهای جدید جایگزین نشد!','title'  : name }
    def getformData(self,request):
        self.result   = request.FILES.get('result')
        self.result2  = request.FILES.get('result2')
        self.result3  = request.FILES.get('result3')
    def checkEmptyUploadedFiles(self, request, name):
        if (not(self.result or self.result2 or self.result3)):
            self.context = {'reserve' : self.reserve, 'title': name }
    def saveResults(self,request,name):
        self.reserve.result  = self.result
        self.reserve.result2 = self.result2
        self.reserve.result3 = self.result3
        self.reserve.save()
        self.context = {'message':'نتایج با موفقیت ثبت شد!','title'  : name }

class chooseUserforEditAnalysis(View):
    template_name = 'specialists/analysis/chooseUser.html'
    def get(self, request, name):
        return render (request, self.template_name)
    def post(self, request, name):
        firstname = request.POST['firstname']
        lastname  = request.POST['lastname']
        if (firstname and lastname):
            info = profiledb.objects.filter(firstname__contains=firstname, lastname__contains=lastname)
        elif (firstname):
            info = profiledb.objects.filter(firstname__contains=firstname)
        elif (lastname):
            info = profiledb.objects.filter(lastname__contains=lastname)
        if (info.count()):
            context = {'info': info}
        else:
            context = {'message': "فردی با این مشخصات در سیستم ثبت نشده است!"}
        return render (request, self.template_name, context)

class editAnalysis(View):
    template_name = 'specialists/analysis/editAnalysis.html'
    def get(self, request, name, username):
        self.getCommonInfo (self, name, username)
        if (self.info):
            self.context.update({'info': self.info})
        else:
            self.context.update({'message': 'مراجعه‌ای انجام نشده است!'})
        return render (request, self.template_name, self.context)
    def post(self, request, name, username):
        self.getCommonInfo (self, name, username)
        determiner = request.POST['determiner']
        if (determiner == 'search'):
            PK = request.POST['PK']
            selectedVisit = globals()[self.database].objects.get (pk=PK)
        elif (determiner == 'edit'):
            result   = request.FILES['result']
            year     = request.POST['year']
            month    = request.POST['month']
            day      = request.POST['day']
            order    = request.POST['order']
            selectedVisit = globals()[self.database].objects.get (user=self.user, year=year, month=month, day=day, order=order)
            selectedVisit.result.delete()
            selectedVisit.result = result
            selectedVisit.save()
            self.context.update({'message': 'فایل با موفقیت ویرایش شد.'})
        self.context.update({'selectedVisit': selectedVisit, 'info': self.info})
        return render (request, self.template_name, self.context)
        
    def getCommonInfo (self, request, name, username):
        self.user = User.objects.get(username=username)
        profileInfo = profiledb.objects.get(user=self.user)
        firstcontext = {'profileInfo': profileInfo}
        self.context = firstcontext.copy()
        self.database = name.lower()+'reservation'
        self.info = globals()[self.database].objects.filter (user=self.user, visit=True).exclude(duration="1").order_by('year','month','day','order')



"""wellness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

from index.views import *
from wellness.views import *
from authapp.views import *
from reservation.views import *
from shop.views import *
from zarinpal.views import *
from quiz.views import *
from specialists.views import *
from ticket.views import *

from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
import debug_toolbar

from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'snippet': StaticViewSitemap
}

urlpatterns = [
    
    path(r'sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('admin/', admin.site.urls),
    path(r'__debug__/', include(debug_toolbar.urls)),
    
    ## صفحه اصلی وب‌اپ
    path('', TemplateView.as_view(template_name="index/index.html"), name="index"),
    
    ##
    path(r'auth/', include('authapp.urls')),
    
    ## عضویت کاربر
    path(r'phoneverification/', phoneverification, name="phoneverification"),
    path(r'activation/', activation, name="activation"),
    
    ## ورود و خروج پنل کاربری
    path(r'login/' , login_view, name="login"),
    path(r'logout/', logout_view),
    
    ## صفحه اصلی پنل کاربری
    path(r'dashboard/' , dashboard, name="dashboard"),

    ## ارتباط با ما
    path(r'contact/' , TemplateView.as_view(template_name="index/contactus.html"), name="contact"),

    ## معرفی ولنس
    path(r'introduction/', TemplateView.as_view(template_name="index/introduction.html"), name="introduction"),
    
    ## اخبار ولنسی
    path('news/', include('news.urls')),
    # path('news/blog/', include('news.urls')),
    ## عضویت ویژه
    path(r'membership/',membership, name="membership"),
    path(r'membership/plans/', login_required(TemplateView.as_view(template_name="authapp/membershipPlans.html")), name="membershipplans"),
    path(r'membership/plans/<str:planType>',PlanType),
    
    ## مشخصات کاربر
    path(r'dashboard/profile/', profile, name="profile"),
    
    ## پشتیبانی حضوری پنل کاربری
    path(r'dashboard/services/', services, name="services"),
    path(r'dashboard/services/<str:slug>/',serviceoptions),
    path(r'dashboard/services/<str:servicetype>/results', resultservices),
    
    
    path(r'dashboard/services/queueHealth/reserve/', daychoose),
    path(r'dashboard/services/queueHealth/reserve/<int:year>/<int:month>/<int:day>/',timechoose),
    path(r'dashboard/services/queueHealth/reserve/<int:year>/<int:month>/<int:day>/<int:duration>',search),
    path(r'dashboard/services/queueHealth/reserve/<int:year>/<int:month>/<int:day>/<int:duration>/<int:order>',result),

    path(r'dashboard/services/queueResonance/reserve/', daychoose),
    path(r'dashboard/services/queueResonance/reserve/<int:year>/<int:month>/<int:day>/',timechoose),
    path(r'dashboard/services/queueResonance/reserve/<int:year>/<int:month>/<int:day>/<int:duration>',search),
    path(r'dashboard/services/queueResonance/reserve/<int:year>/<int:month>/<int:day>/<int:duration>/<int:order>',result),
    
    path(r'monthinfo/<int:idx>',monthinfo),


    ## فروشگاه
    path(r'dashboard/shop/', include("shop.urls")),
    
    ## انتقادها و پیشنهادها
    path(r'dashboard/comments', commentitems, name="commentitems"),
    path(r'dashboard/comments/<str:item>', comments),
    
    
    ## ارزیابی ها پنل کاربری
    path(r'dashboard/evaluation/', evaluation, name="evaluation"),
    path(r'dashboard/evaluation/quiz/', quizlist, name="quizlist"),
    ##توضیحات 12 بعد
    path(r'dashboard/evaluation/quiz/quiz-introduction/<int:quiz_number>',QuizIntroduction),
    path(r'dashboard/evaluation/quiz/<int:quiz_number>',quiz),
    path(r'quiz/article/<int:quiz_number>/<int:question_number>',article),
    path(r'dashboard/evaluation/quizresult/',quizresult, name="quizresult"),
    
    ## پرداخت ها
    path(r'dashboard/payments/', payments, name="payments"),
    path(r'send_request/', send_request),
    path(r'verify/', verify),

    ## پیگیری‌ها
    path(r'dashboard/ticket/',include('ticket.urls')),
    
    
    ##### پنل مدیریت
    path(r'MSlogin/', MSlogin),
    path(r'manager/', include("manager.urls")),
    
    ##### پنل متخصص
    path(r'specialists/',include('specialists.urls')),
]


#urlpatterns += static(settings.STATIC_URL,  document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL,   document_root=settings.MEDIA_ROOT)


from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from random import randint
from django.utils import timezone
from datetime import datetime
from manager.DateConverter import *
from authapp.models import profiledb
from zarinpal.models import *
from index.models import *
from manager.models import *

from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

    
class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return['phoneverification', 'activation', 'login','dashboard', 'membership', 'membershipplans', 'profile', 'shop', 'contact', 'introduction']
        
    def location(self, item):
        return reverse(item)

def display_meta(request):
    values = request.META.items()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(ip)

def error_404(request, exception):
    data = {}
    return render(request,'index/404.html', data)

def error_500(request):
    data = {}
    return render(request,'index/500.html', data)
    
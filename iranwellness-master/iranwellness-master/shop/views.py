from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from shop.models import *
from authapp.models import profiledb
@login_required(redirect_field_name='', login_url='/login/')
def shop(request):
    user=request.user
    try:
        info= profiledb.objects.get(user=user)
        status= "valid"
    except ObjectDoesNotExist:
        status= "invalid"
    return render(request, 'shop/shop.html', {'status':status})
    
@login_required(redirect_field_name='', login_url='/login/')
def products(request,Type):
    user=request.user
    PS= Shoppingitem.objects.filter(ptype= Type)
    if request.method == 'POST':
        price=int(request.POST.get('fee'))
        name =    request.POST.get('Name')
        Pname=    request.POST.get('Pname')
        ShoppingReceipt.objects.create(user=user, name=name, price=price, Pname=Pname)
        info=ShoppingReceipt.objects.filter(user=user)
        return render(request, 'shop/' + Type +'/'+ Type + '.html',{'info': info,
                                                                    'PS'  : PS})
    else:
        try:
            info=ShoppingReceipt.objects.filter(user=user)
            return render(request, 'shop/' + Type +'/'+ Type + '.html',{'info': info,
                                                                                 'PS'  :PS})
        except ObjectDoesNotExist:
            return render(request, 'shop/' + Type +'/'+ Type + '.html',{'PS':PS})
    return HttpResponse('Physical')

def InformationOfProducts(request,Type,Name):
    return render(request, 'zarinpal/shop/' + Type +'/'+ Name + 'Abs.html')

@login_required(redirect_field_name='', login_url='/login/')
def cart(request):
    user=request.user
    if request.method == 'POST':
        name =    request.POST.get('name')
        price=int(request.POST.get('price'))
        ShoppingReceipt.objects.get(user=user, name=name, price=price).delete()
        inf=ShoppingReceipt.objects.filter(user=user, paid=False)
        if (len(inf) == 0):
            return render(request, 'shop/cart.html',{'message': 'سبد خرید شما خالی است'})
        else:
            return render(request, 'shop/cart.html',{'info': inf})
    else:
        inf=ShoppingReceipt.objects.filter(user=user, paid=False)
        return render(request, 'shop/cart.html',{'info': inf})
    
@login_required(redirect_field_name='', login_url='/login/')
def YourProducts(request,Type,Name):
    return render(request, 'shop/'+Type+'/'+Name+'.html')
#def shopCategory(request):
#  model = Title
#  info = model.objects.all()
#  context = {'info': info}
#  template_name = 'shop/shopCategory.html'
#  return render(request, template_name, context)

#def shopSubCategory(request, category):
#  model= FirstShoppingCategory
#  title=Title.objects.get(Ename=category)
#  info = model.objects.filter(title=title)
#  context = {'info': info, 'title':title}
#  template_name = 'shop/shopSubCategory.html'
#  return render(request, template_name, context)

#def shopSubCategory2(request, category):
#  model1= FirstShoppingCategory
#  model2= Product
#  info = model1.objects.filter(title=Title.objects.get(Ename=category))
#  products = model2.objects.filter(firstShoppingCategory= info[0])
#  if (products):
#    context= 'دارد'
#  else:
#    context= 'ندارد'
#  return HttpResponse(context)
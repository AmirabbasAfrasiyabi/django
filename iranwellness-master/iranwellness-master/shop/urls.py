from django.urls import path
from .views import *

urlpatterns = [
    path(r'', shop, name="shop"),
    #path(r'shop/<str:Type>/',products),
    #path(r'shop/<str:Type>/<str:Name>/', InformationOfProducts),
    #path(r'cart/', cart, name="shoppingcart"),
    #path(r'sendcartRequest/',send_cartRequest),
    #path(r'cartverify/',cartverify),
    #path(r'shop/<str:Type>/<str:Name>/YP/', YourProducts),
    #path(r'dashboard/shop/', shop),
    #path(r'dashboard/shop/products/',shopCategory),
    #path(r'dashboard/shop/products/<str:category>/',shopSubCategory),
    #path(r'shop/<str:Type>/',products),
    #path(r'shop/<str:Type>/<str:Name>/', InformationOfProducts),
    #path(r'cart/', cart),
    #path(r'sendcartRequest/',send_cartRequest),
    #path(r'cartverify/',cartverify),
    #path(r'shop/<str:Type>/<str:Name>/YP/', YourProducts), 
]
from django.db import models

class Title(models.Model):
  Ename = models.CharField(max_length=50)
  Pname = models.CharField(max_length=50)
  order = models.IntegerField(null=True)
  def __str__(self):
        return self.Pname

class FirstShoppingCategory(models.Model):
  title       = models.ForeignKey(Title, on_delete=models.CASCADE, null=True)
  Ename       = models.CharField(max_length=50)
  Pname       = models.CharField(max_length=50)
  price       = models.IntegerField(null=True, blank=True)
  image       = models.ImageField(upload_to='FirstCategoryShop_image',  null=True, blank=True) # تصویر محصول
  def __str__(self):
        return self.Pname

class Product(models.Model):
  firstShoppingCategory = models.ForeignKey(FirstShoppingCategory, on_delete=models.CASCADE, null=True)
  Ename                 = models.CharField(max_length=50)
  Pname                 = models.CharField(max_length=50)
  website               = models.CharField(max_length=50)
  Link                  = models.URLField(max_length = 200, null=True, blank=True) 
  price                 = models.IntegerField(null=True, blank=True)
  def __str__(self):
        return self.Pname

#class Shoppingitem(models.Model):
#      Ename = models.CharField(max_length=20)
#      Pname = models.CharField(max_length=20)
#      ptype = models.CharField(max_length=20)
#      price = models.IntegerField()
#      
#      def __str__(self):
#        return self.Pname

#class ShoppingReceipt(models.Model):
#      user =models.ForeignKey(User,on_delete=models.CASCADE)
#      name =models.CharField(max_length=20)
#      Pname=models.CharField(max_length=20)
#      paid =models.BooleanField(default=False)
#      price=models.IntegerField() 
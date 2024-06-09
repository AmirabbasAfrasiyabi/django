from django.db import models
from django.contrib.auth.models import User

#class ShoppingReceipt(models.Model):
#      user =models.ForeignKey(User,on_delete=models.CASCADE)
#      name =models.CharField(max_length=20)
#      Pname=models.CharField(max_length=20)
#      paid =models.BooleanField(default=False)
#      price=models.IntegerField()

class PhysicalShoppingitem(models.Model):
      Ename=models.CharField(max_length=20)
      Pname=models.CharField(max_length=20)
      price=models.IntegerField()
      
      def __str__(self):
        return self.Pname
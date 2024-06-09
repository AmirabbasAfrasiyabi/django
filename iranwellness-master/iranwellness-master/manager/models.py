from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from jdatetime import date as jd


class quickreceipt(models.Model):
      firstname   = models.CharField     (max_length=20,null=True)  #نام
      lastname    = models.CharField     (max_length=20,null=True)  #نام خانوادگی
      title       = models.CharField     (max_length=20,null=True)  #موضوع
      fee         = models.CharField     (max_length=20,null=True)  #مبلغ
      phone       = models.CharField     (max_length=11,null=True) #شماره همراه
      explane     = models.CharField     (max_length=254,null=True) #توضیحات
      time_created= models.DateTimeField (default=now) #تاریخ ثبت فاکتور
      time_paied  = models.DateTimeField (null=True)# تاریخ پرداخت فاکتور
      
      def j_date_created(self):
          jdate=jd.fromgregorian(
                     year   =self.time_created.year,
                     month  =self.time_created.month,
                     day    =self.time_created.day,
                     )
          return jdate.strftime('%d %B %Y')
      
      def j_date_paied(self):
          jdate=jd.fromgregorian(
                     year   =self.time_paied.year,
                     month  =self.time_paied.month,
                     day    =self.time_paied.day,
                     )
          return jdate.strftime('%d %B %Y')  
      
      def __str__(self):
        return self.lastname
        
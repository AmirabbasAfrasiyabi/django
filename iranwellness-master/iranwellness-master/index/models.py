from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jdatetime import date as jd


# comments
class comment(models.Model):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.IntegerField()
    branch  = models.IntegerField()
    text    = models.CharField(max_length=300)
    date    = models.DateTimeField (default=timezone.now, blank=True)
    
    def j_date(self):
          jdate=jd.fromgregorian(
                     year   =self.date.year,
                     month  =self.date.month,
                     day    =self.date.day,
                     )
          return jdate.strftime('%d %B %Y')
      
    def __str__(self):
        return str(self.user)
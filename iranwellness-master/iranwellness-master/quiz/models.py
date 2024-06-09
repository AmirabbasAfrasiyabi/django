from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jdatetime import date as jd

class submit(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    number      = models.IntegerField  (default=0)
    date        = models.DateTimeField (default=timezone.now)
    response    = models.CharField     (max_length=50,default="")
    result      = models.CharField     (max_length=5000,default="")
    imageresult = models.ImageField    (upload_to='quiz_results_12dimensions/image',      null=True, blank=True)
    pdfresult   = models.FileField     (upload_to='quiz_results_12dimensions/file',       null=True, blank=True)
    audioresult = models.FileField     (upload_to='quiz_results_12dimensions/audio',      null=True, blank=True)
    videoresult = models.FileField     (upload_to='quiz_results_12dimensions/video',      null=True, blank=True)
    
    def j_date_submit(self):
          jdate=jd.fromgregorian(
                     year   =self.date.year,
                     month  =self.date.month,
                     day    =self.date.day,
                     )
          return jdate.strftime('%d %B %Y')
      
    def __str__(self):
        return "{} | {} | {}".format(self.user,self.number,self.date)

class wellnessCircle(models.Model):
    user        = models.ForeignKey    (User,on_delete=models.CASCADE,null=True)
    date        = models.DateTimeField (default=timezone.now)
    totalquiz   = models.CharField     (max_length=100,default="")
    result      = models.CharField     (max_length=5000,default="")
    imageresult = models.ImageField    (upload_to='quiz_results_wellnessCircle/image',    null=True, blank=True)
    pdfresult   = models.FileField     (upload_to='quiz_results_wellnessCircle/file',     null=True, blank=True)
    audioresult = models.FileField     (upload_to='quiz_results_wellnessCircle/audio',    null=True, blank=True)
    videoresult = models.FileField     (upload_to='quiz_results_wellnessCircle/video',    null=True, blank=True)
    
    def j_date_circle(self):
          jdate=jd.fromgregorian(
                     year   =self.date.year,
                     month  =self.date.month,
                     day    =self.date.day,
                     )
          return jdate.strftime('%d %B %Y')
      
    def __str__(self):
        return str(self.user)
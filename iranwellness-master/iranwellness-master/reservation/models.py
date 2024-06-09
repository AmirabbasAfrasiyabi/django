from django.db import models
from django.contrib.auth.models import User


class dayoff(models.Model):
    year  = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day   = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.year}/{self.month}/{self.day}'
    
    class Meta:
        ordering = ['year','month','day']
        verbose_name = "روز تعطیل"
        verbose_name_plural = "روزهای تعطیل"

class healthreservation(models.Model):
    user       = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    year       = models.IntegerField(default=0)
    month      = models.IntegerField(default=0)
    day        = models.IntegerField(default=0)
    order      = models.IntegerField(default=0)
    duration   = models.IntegerField(default=0)
    string     = models.CharField(max_length=50,default="")
    paid       = models.BooleanField(default=False)
    visit      = models.BooleanField(default=False)
    time_paied = models.DateTimeField (null=True)
    result     = models.FileField (upload_to='health_results', default="", blank=True)
    result2    = models.FileField (upload_to='health_results', default="", blank=True)
    result3    = models.FileField (upload_to='health_results', default="", blank=True)
    def __str__(self):
        return self.string
    class Meta:
        verbose_name = "رزرو هلث"
        verbose_name_plural = "رزروهای هلث"
    

class resonancereservation(models.Model):
    CATEGORY_CHOICES = [
        ('Resonance', 'رزونانس'),
        ('Frequency', 'فرکانس')
    ]
    user       = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    year       = models.IntegerField(default=0)
    month      = models.IntegerField(default=0)
    day        = models.IntegerField(default=0)
    order      = models.IntegerField(default=0)
    duration   = models.IntegerField(default=0)
    string     = models.CharField(max_length=50,default="")
    category   = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Resonance')
    paid       = models.BooleanField(default=False)
    visit      = models.BooleanField(default=False)
    time_paied = models.DateTimeField (null=True)
    result     = models.FileField (upload_to='resonance_results', default="", blank=True)
    result2    = models.FileField (upload_to='resonance_results', default="", blank=True)
    result3    = models.FileField (upload_to='resonance_results', default="", blank=True)
    def __str__(self):
        return self.string
    class Meta:
        verbose_name = "رزرو ای‌دی‌اس"
        verbose_name_plural = "رزروهای ای‌دی‌اس"
from django.db import models
from django.contrib.auth.models import User

class sms_verification_table(models.Model):
    ip = models.GenericIPAddressField(default='1.1.1.1')
    phone_number = models.CharField(max_length=12,null=False,blank=False)
    key = models.CharField(max_length=5)
    time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.phone_number
    class Meta:
        verbose_name = "کد فعالسازی"
        verbose_name_plural = "کدهای فعالسازی"


class profiledb(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    wellid         = models.CharField (default="", blank=True, max_length=15, verbose_name="کد ولنسی")
    membershipType = models.CharField (default='Normal', blank=True, max_length=10, verbose_name="نوع عضویت کاربر")
    firstname      = models.CharField (max_length=20, verbose_name="نام", default="")
    lastname       = models.CharField (max_length=20, verbose_name="نام خانوادگی", default="")
    Email          = models.EmailField(default="", blank=True, max_length=254, verbose_name="ایمیل")
    address1       = models.CharField (default="", blank=True, max_length=254, verbose_name="آدرس منزل")
    phone1         = models.CharField (default="", blank=True, max_length=11,  verbose_name="تلفن ثابت")
    job            = models.CharField (default="", blank=True, max_length=20,  verbose_name="شغل")
    address2       = models.CharField (default="", blank=True, max_length=254, verbose_name="آدرس حدودی محل کار")
    phone3         = models.CharField (default="", blank=True, max_length=11,  verbose_name="شماره شبکه‌های اجتماعی")
    image          = models.ImageField(upload_to='ProfileImage', default="", blank=True, verbose_name="تصویر پروفایل")
    isActive       = models.BooleanField(default=True)
       
    def __str__(self):
        return (self.firstname + ' ' + self.lastname)
    class Meta:
        verbose_name = "مشخصات کاربری"
        verbose_name_plural = "مشخصات کاربرها"
    
def user_return_string(self):
    try:
        return self.username+" "+self.profiledb.firstname+" "+self.profiledb.lastname
    except:
        return self.username

User.add_to_class("__str__", user_return_string)
from django.db import models
from django.utils import timezone
from jdatetime import date as jd
from authapp.models import profiledb
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

class Chat(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message          = models.TextField(null=True)
    image            = models.ImageField(upload_to='Ticket_images', null=True,  blank=True)
    content_type     = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id        = models.PositiveIntegerField(null=True)
    content_object   = GenericForeignKey('content_type' , 'object_id')
    create_datetime  = models.DateTimeField(default=timezone.now)
    def jalali_create_date(self):
          jdate=jd.fromgregorian(
                     year   =self.create_datetime.year,
                     month  =self.create_datetime.month,
                     day    =self.create_datetime.day,
                     )
          return jdate.strftime('%d %B %Y')
    def __str__(self):
        return self.message[:30] or ''

class TicketOnServices(models.Model):
    STATUS_list = [
        ('open', 'باز'),
        ('closed', 'بسته‌شده')
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    service    = models.ForeignKey("services.serviceModel", on_delete=models.PROTECT, verbose_name="خدمت")
    topic      = models.CharField(max_length=200, verbose_name="موضوع تیکت")
    chats      = GenericRelation(Chat, null=True)
    status     = models.CharField(max_length=20, choices=STATUS_list, default="open", verbose_name="وضعیت")
    def __str__(self):
        return self.topic or ''
    class Meta:
        verbose_name = "تیکت مربوط به خدمات"
        verbose_name_plural = "تیکت‌های مربوط به خدمات"   
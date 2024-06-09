from django.db import models

class serviceModel(models.Model):
  name = models.CharField(max_length=50, verbose_name="نام خدمت")
  slug = models.SlugField(max_length=200, verbose_name="اسلاگ خدمت")
  thumbnail_service=models.ImageField(upload_to='service-thumbnails', blank=True, null=True, verbose_name="تصویر شاخص")
  def __str__(self):
    return self.name
  class Meta:
    verbose_name = "مشخصات خدمت"
    verbose_name_plural = "مشخصات خدمات"
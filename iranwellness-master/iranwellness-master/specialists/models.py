from django.db import models

# Create your models here.
class test(models.Model):
    job = models.CharField (max_length=20, null=True)
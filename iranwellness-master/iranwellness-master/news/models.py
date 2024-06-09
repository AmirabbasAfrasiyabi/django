from django.db import models

class new (models.Model):
    Pname   = models.CharField(max_length=50, null=True)
    Ename   = models.CharField(max_length=50, null=True)
    def __str__(self):
        return str(self.Pname)

class subject (models.Model):
    new = models.ForeignKey(new, on_delete=models.CASCADE, null=True)
    Pname   = models.CharField(max_length=70, null=True)
    Ename   = models.CharField(max_length=70, null=True)
    def __str__(self):
        return str(self.Pname)

class topic (models.Model):
    subject = models.ForeignKey(subject, on_delete=models.CASCADE, null=True)
    Pname   = models.CharField(max_length=70, null=True)
    Ename   = models.CharField(max_length=70, null=True)
    order   = models.IntegerField(null=True)
    def __str__(self):
        return str(self.Pname)
from django.db import models
from django.contrib.auth.models import User

class Work(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    salary = models.PositiveSmallIntegerField()
    tax_percent = models.PositiveSmallIntegerField()
    extra_public_holiday_percent= models.PositiveSmallIntegerField()
    extra_per_day = models.PositiveSmallIntegerField()
    extra_additional_hour_percent = models.PositiveSmallIntegerField()

class WorkHour(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    beginning_date = models.DateTimeField()
    end_date = models.DateTimeField()



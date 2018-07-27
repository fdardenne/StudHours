from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserCreationForm
import datetime

class Work(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    salary = models.DecimalField(decimal_places=2, max_digits=5)
    tax_percent = models.DecimalField(decimal_places=2, max_digits=5)
    extra_public_holiday_percent= models.DecimalField(decimal_places=2, max_digits=5)
    extra_per_day = models.DecimalField(decimal_places=2, max_digits=5)

class WorkHour(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    beginning_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pause_duration = models.DurationField(default=datetime.timedelta(days=0))
    public_holiday = models.BooleanField(default=False)
    salary_earned = models.DecimalField(decimal_places=2, max_digits=6, default=0)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


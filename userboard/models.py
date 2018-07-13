from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

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

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


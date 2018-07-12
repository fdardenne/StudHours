from django.db import models
from django.contrib.auth.models import User

class Work(models.Model):
    beginning_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)

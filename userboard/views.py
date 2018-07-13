from django.shortcuts import render
from .models import Work, WorkHour
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def userboard(request):
    moneys = [100,0,110,90,0,0,0,70,100,105,0,110,110,90,80,100,0,70,100,105,100,0,110,0,80,100,120,0,100,105]
    context = {
        'id': 1,
        'total_month_money': sum(moneys),
        'total_month_hours':120,
        'day': range(1,31),
        'money': moneys,
    }
    return render(request, 'userboard/dashboard.html', context)

def homepage(request):
    return render(request, 'userboard/homepage.html')
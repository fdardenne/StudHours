from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import SignUpForm
from .models import Work, WorkHour
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# Create your views here.

@login_required
def userboard(request):
    work = Work.objects.get(user=request.user)
    wks_list = WorkHour.objects.filter(work=work)
    print(work)
    print(wks_list)
    moneys = [100,0,110,90,0,0,0,70,100,105,0,110,110,90,80,100,0,70,100,105,100,0,110,0,80,100,120,0,100,105]
    context = {
        'id': 1,
        'total_month_money': sum(moneys),
        'total_month_hours':120,
        'day': range(1,31),
        'money': moneys,
    }
    return render(request, 'userboard/dashboard.html', context)

@login_required
def profile(request):
    user = request.user
    name = user.username
    email = user.email
    first_name = user.first_name
    last_name = user.last_name

    information = {
        'username': name,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    }
    return render(request, 'userboard/user.html', information)

def homepage(request):
    return render(request, 'userboard/homepage.html')



def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('userboard')
        return render(request, 'registration/signup.html', {'form': form})

    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})



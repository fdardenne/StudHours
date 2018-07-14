from django.shortcuts import render, redirect
from .models import SignUpForm
from .models import Work, WorkHour
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
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

@login_required
def work(request):
    if request.method == "POST":
        print(request.POST.get('name'))
        print((Work.objects.filter(user = request.user)))
        context = {}
        if len(Work.objects.filter(user = request.user)) == 0:
            work = Work(user=request.user, name=request.POST.get('name'),
                        salary=request.POST.get('price'),
                        tax_percent=request.POST.get('tax'),
                        extra_public_holiday_percent=request.POST.get('holiday'),
                        extra_per_day=request.POST.get('extra'),
                        extra_additional_hour_percent = request.POST.get('extra_add'))
            work.save()

        else:
            #TODO NOTIFY THE USER
            work = Work.objects.get(user=request.user)
            context = {'name': work.name, 'salary': work.salary,
                       'tax': work.tax_percent, 'extra_public_holiday': work.extra_public_holiday_percent,
                       'extra_day': work.extra_per_day, }

            work.name =request.POST.get('name')
            work.salary = request.POST.get('price')
            work.tax_percent =  request.POST.get('tax')
            work.extra_public_holiday_percent = request.POST.get('holiday')
            work.extra_per_day = request.POST.get('extra')
            work.extra_additional_hour_percent = request.POST.get('extra_add')
            work.save()


    return render(request, 'userboard/work.html', context)

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



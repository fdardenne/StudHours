from django.shortcuts import render, redirect
from .models import SignUpForm
from .models import Work, WorkHour
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import datetime
import calendar
# Create your views here.

@login_required
def userboard(request):

    day_max = calendar.monthrange(datetime.datetime.now().date().year, datetime.datetime.now().date().month)[1]

    user = request.user
    work = Work.objects.get(user=user)
    workhour_month_list = WorkHour.objects.filter(work=work, beginning_date__month=datetime.datetime.now().date().month)

    moneys = [0] * day_max

    total_money = 0
    total_hours = 0

    for workhour in workhour_month_list:
        day = workhour.beginning_date.date().day
        time_worked = float((workhour.end_date - workhour.beginning_date).seconds) / 3600
        money_earned = time_worked * float(work.salary)

        total_hours += time_worked
        total_money += round(time_worked * float(work.salary),2)
        moneys[day-1] += round(money_earned, 2)



    color_template = ["rgba(255, 99, 132, 0.2)",
                      "rgba(54, 162, 235, 0.2)",
                      "rgba(255, 206, 86, 0.2)",
                      "rgba(75, 192, 192, 0.2)",
                      "rgba(153, 102, 255, 0.2)",
                      "rgba(255, 159, 64, 0.2)",
                      "rgba(244, 66, 244,0.2)"]

    border_color_template = ['rgba(255,99,132,1)',
                             'rgba(54, 162, 235, 1)',
                             'rgba(255, 206, 86, 1)',
                             'rgba(75, 192, 192, 1)',
                             'rgba(153, 102, 255, 1)',
                             'rgba(255, 159, 64, 1)',
                             'rgba(244, 66, 244, 1)',
                             ]

    label = []
    color = []
    border_color = []

    first_day_week = calendar.monthrange(datetime.datetime.now().date().year, datetime.datetime.now().date().month)[0]

    #BUILD CONTEXT
    for x in range(day_max):
        label.append(x+1)

        first_day_week = 0 if first_day_week == 7 else first_day_week
        color.append(color_template[first_day_week])
        border_color.append(border_color_template[first_day_week])
        first_day_week += 1

    context = {
        'day': label,
        'money': moneys,
        'color': color,
        'border_color': border_color,
        'total_money': total_money,
        'total_hours': total_hours
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
    #TODO Verify the form
    work_list = Work.objects.filter(user=request.user)
    flag = ''
    if request.method == "POST":
        if len(work_list) == 0:

            new_work = Work(user=request.user, name=request.POST.get('name'),
                        salary=request.POST.get('price'),
                        tax_percent=request.POST.get('tax'),
                        extra_public_holiday_percent=request.POST.get('holiday'),
                        extra_per_day=request.POST.get('extra'),
                        extra_additional_hour_percent = request.POST.get('extra_add'))
            new_work.save()
            flag = 'created'

        else:
            work_modified = Work.objects.get(user=request.user)
            work_modified.name =request.POST.get('name')
            work_modified.salary = request.POST.get('price')
            work_modified.tax_percent =  request.POST.get('tax')
            work_modified.extra_public_holiday_percent = request.POST.get('holiday')
            work_modified.extra_per_day = request.POST.get('extra')
            work_modified.extra_additional_hour_percent = request.POST.get('extra_add')
            work_modified.save()
            flag = 'modified'

    try:
        work = Work.objects.filter(user=request.user)[0]
        context = {'name': work.name,
                    'salary': work.salary,
                    'tax': work.tax_percent,
                    'extra_public_holiday': work.extra_public_holiday_percent,
                    'extra_additional_hour': work.extra_additional_hour_percent,
                    'extra_day': work.extra_per_day,
                    'flag': flag,
                    }
    except:
        context = {}
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

@login_required
def hour(request):
    #TODO VERIFY THE FORM

    user = request.user
    work = Work.objects.get(user=user)

    if request.method == "POST":

        begin_date_hour_list = request.POST.get("beginning").split("T")
        begin_date_list = begin_date_hour_list[0].split('-')
        begin_hour_list = begin_date_hour_list[1].split(':')

        end_date_hour_list = request.POST.get("end").split("T")
        end_date_list = end_date_hour_list[0].split('-')
        end_hour_list = end_date_hour_list[1].split(':')

        begin_date = datetime.datetime(day=int(begin_date_list[2]), month=int(begin_date_list[1]),
                                       year=int(begin_date_list[0]), minute=int(begin_hour_list[1]),
                                       hour=int(begin_hour_list[0]))

        end_date = datetime.datetime(day=int(end_date_list[2]), month=int(end_date_list[1]),
                                       year=int(end_date_list[0]), minute=int(end_hour_list[1]),
                                       hour=int(end_hour_list[0]))

        new_hour = WorkHour(work=work, beginning_date=begin_date, end_date=end_date)
        new_hour.save()

    workhours_list = WorkHour.objects.filter(work=work)
    context_list = []
    for hours in workhours_list:
        context_list.append({
            'beginning_date':hours.beginning_date.strftime("%d/%m/%y %H:%M"),
            'end_date':hours.end_date.strftime("%d/%m/%y %H:%M"),
            'time': float((hours.end_date-hours.beginning_date).seconds)/3600,
        })

    context = {'workhours_list': context_list}



    return render(request, 'userboard/hours.html', context)



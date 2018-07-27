from django.shortcuts import render, redirect
from .models import SignUpForm
from .models import Work, WorkHour
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import datetime
import calendar


def handler404(request):
    print("4004")
    return render(request, 'error/404.html', status=404)


def handler500(request):
    return render(request, 'error/404.html', status=500)

# Reveal.js welcome page
def homepage(request):
    return render(request, 'userboard/homepage.html')


#Registration page
def signup(request):
    if request.method == 'POST':
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
def userboard(request):
    # init variables
    first_day_week, day_max = calendar.monthrange(datetime.datetime.now().date().year, datetime.datetime.now().date().month)

    label = []
    color = []
    border_color = []

    color_template = ['rgba(255, 99, 132, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(255, 206, 86, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(153, 102, 255, 0.2)',
                      'rgba(255, 159, 64, 0.2)',
                      'rgba(244, 66, 244,0.2)']

    border_color_template = ['rgba(255,99,132,1)',
                             'rgba(54, 162, 235, 1)',
                             'rgba(255, 206, 86, 1)',
                             'rgba(75, 192, 192, 1)',
                             'rgba(153, 102, 255, 1)',
                             'rgba(255, 159, 64, 1)',
                             'rgba(244, 66, 244, 1)',
                             ]

    # build chart label / color / border color
    for day_number in range(1, day_max+1):
        label.append(day_number)

        #for the color
        first_day_week = 0 if first_day_week == 7 else first_day_week
        color.append(color_template[first_day_week])
        border_color.append(border_color_template[first_day_week])
        first_day_week += 1



    # get database information
    try:
        user = request.user
        work = Work.objects.get(user=user)
        workhour_month_list = WorkHour.objects.filter(work=work,
                                                      beginning_date__month=datetime.datetime.now().date().month,
                                                      beginning_date__year= datetime.datetime.now().date().year)


        moneys = [0] * day_max
        month_total_money = 0
        month_total_hours = 0

        money_per_month = [0]*12
        total_money_year = 0
        total_hours_year = 0

        for workhour in workhour_month_list:
            day = workhour.beginning_date.date().day
            time_worked = float((workhour.end_date - workhour.beginning_date - workhour.pause_duration).seconds) / 3600
            money_earned = float(round(workhour.salary_earned, 2))

            month_total_hours += time_worked
            month_total_money += money_earned
            moneys[day-1] += money_earned


        temps_total_money = 0
        for month in range(12):
            temp_workhour_month_list = WorkHour.objects.filter(work=work, beginning_date__month=month,
                                                               beginning_date__year =datetime.datetime.now().date().year)

            for workhour in temp_workhour_month_list:
                time_worked = float(
                    (workhour.end_date - workhour.beginning_date - workhour.pause_duration).seconds) / 3600
                money_earned = float(round(workhour.salary_earned, 2))

                temps_total_money += money_earned

                total_money_year += money_earned
                total_hours_year += time_worked

            money_per_month[month-1] = temps_total_money
            temps_total_money = 0





        context = {
            'day': label,
            'money': moneys,
            'color': color,
            'border_color': border_color,
            'total_money': round(month_total_money,2),
            'total_hours': round(month_total_hours,2),
            'year_total_money': round(month_total_money, 2),
            'year_total_hours': round(month_total_hours, 2),

            'months_money': money_per_month
        }

        return render(request, 'userboard/dashboard.html', context)

    except:
        return render(request, 'userboard/dashboard.html', {'day': label, 'money': [], 'color':color, 'border_color': border_color, 'total_money': 0, 'total_hours': 0, 'months_money':[]})


@login_required
def profile(request):
    user = request.user
    information = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, 'userboard/user.html', information)


@login_required
def work(request):
    # TODO: Verify the form
    work_list = Work.objects.filter(user=request.user)
    flag = ''
    if request.method == 'POST':
        if len(work_list) == 0:

            new_work = Work(user=request.user, name=request.POST.get('name'),
                        salary=request.POST.get('price'),
                        tax_percent=request.POST.get('tax'),
                        extra_public_holiday_percent=request.POST.get('holiday'),
                        extra_per_day=request.POST.get('extra'),)
            new_work.save()
            flag = 'created'

        else:
            work_modified = Work.objects.get(user=request.user)
            work_modified.name = request.POST.get('name')
            work_modified.salary = request.POST.get('price')
            work_modified.tax_percent = request.POST.get('tax')
            work_modified.extra_public_holiday_percent = request.POST.get('holiday')
            work_modified.extra_per_day = request.POST.get('extra')
            work_modified.save()
            flag = 'modified'

    try:
        work = Work.objects.filter(user=request.user)[0]
        context = {'name': work.name,
                    'salary': work.salary,
                    'tax': work.tax_percent,
                    'extra_public_holiday': work.extra_public_holiday_percent,
                    'extra_day': work.extra_per_day,
                    'flag': flag,
                    }
    except:
        context = {}
    return render(request, 'userboard/work.html', context)


@login_required
def hour(request):
    # TODO: Delete button
    user = request.user
    try:
        work = Work.objects.get(user=user)
    except:
        return render(request, 'userboard/hours.html', {'flag': 'error'})

    if request.method == 'POST':
        is_valid = True

        # getting the POST information
        try:

            is_public_holiday = request.POST.get('public_holiday')

            if is_public_holiday and is_public_holiday != "True":
                is_valid = False
            elif not is_public_holiday:
                is_public_holiday = False
            else:
                is_public_holiday = True

            pause = request.POST.get('pause')

            if int(pause) < 0:
                is_valid = False

            begin_date_hour_list = request.POST.get('beginning').split('T')
            end_date_hour_list = request.POST.get('end').split('T')

            # formating data
            duration_pause = datetime.timedelta(minutes=int(pause))
            begin_date_list = begin_date_hour_list[0].split('-')
            begin_hour_list = begin_date_hour_list[1].split(':')

            end_date_list = end_date_hour_list[0].split('-')
            end_hour_list = end_date_hour_list[1].split(':')

            begin_date = datetime.datetime(day=int(begin_date_list[2]), month=int(begin_date_list[1]),
                                           year=int(begin_date_list[0]), minute=int(begin_hour_list[1]),
                                           hour=int(begin_hour_list[0]))

            end_date = datetime.datetime(day=int(end_date_list[2]), month=int(end_date_list[1]),
                                         year=int(end_date_list[0]), minute=int(end_hour_list[1]),
                                         hour=int(end_hour_list[0]))
        except:
            is_valid = False

        if not is_valid:
            return redirect('hour')

        salary_earned = round((float((end_date - begin_date - duration_pause).seconds) / 3600) * float(work.salary), 2)
        if is_public_holiday:
            salary_earned += salary_earned * float(work.extra_public_holiday_percent/100)
        salary_earned += float(work.extra_per_day)
        # Creating and saving the object
        new_hour = WorkHour(work=work, beginning_date=begin_date, end_date=end_date, salary_earned=salary_earned,
                            public_holiday=is_public_holiday,
                            pause_duration=duration_pause)
        new_hour.save()

    if request.GET.get("Delete"):
        wkh= WorkHour.objects.get(pk=int(request.GET.get('id')))
        if wkh.work.user == user:
            wkh.delete()

        return redirect('hour')


    # Show table
    workhours_list = WorkHour.objects.filter(work=work).order_by('-beginning_date')
    context_list = []

    for hours in workhours_list:
        context_list.append({
            'beginning_date': hours.beginning_date.strftime('%d/%m/%y %H:%M'),
            'end_date': hours.end_date.strftime('%d/%m/%y %H:%M'),
            'time': round(float((hours.end_date - hours.beginning_date - hours.pause_duration).seconds) / 3600, 2),
            'salary': hours.salary_earned,
            'pause': hours.pause_duration,
            'id': hours.pk
        })

    return render(request, 'userboard/hours.html', {'workhours_list': context_list})

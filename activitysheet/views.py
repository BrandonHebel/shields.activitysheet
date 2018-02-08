from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user

from .models import DailyActivitySheet, Activity, Person
from .forms import ActivityForm
from datetime import datetime
import calendar

def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    # "If there is already a daily activity sheet for today, add to / complete it.  Otherwise create a new daily activity sheet."
    activitysheet = DailyActivitySheet.objects.filter(date=datetime.now()).filter(user=get_user(request)).first()
    if activitysheet:
        activities = activitysheet.activity_set.all()
    else:
        # @TODO change person equal to user after learning django authentication
        activitysheet = DailyActivitySheet(user=get_user(request), date=datetime.now())
        activitysheet.save()
        activities = {}

    form = ActivityForm()
    context = { 'activities': activities, 'form': form,
                'day_of_week' : calendar.day_name[activitysheet.date.weekday()],
                'activitysheet' : activitysheet }

    return render(request, 'activitysheet/index.html', context)

@require_POST
def addActivity(request, activitysheet_id):

    #post['start_time'] = convertTime(post['start_time'])
    #post['end_time'] = convertTime(post['end_time'])
    form = ActivityForm(request.POST)

    if form.is_valid():
        new_activity = Activity(
            activitysheet=DailyActivitySheet.objects.get(pk=activitysheet_id),
            name=form.cleaned_data['name'],
            start_time=form.cleaned_data['start_time'],
            end_time=form.cleaned_data['end_time'])
        new_activity.save()

    return redirect('index')

def viewSheets(request):
    return render(request, 'activitysheet/view_sheets.html')

# convertTime accepts a string in the format 1:30 PM and returns a string in format 13:30
def convertTime(time):
	time = datetime.strptime(time, '%I:%M %p')
	return time.strftime('%H:%M')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {'form' : form}
    return render(request, 'registration/register.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

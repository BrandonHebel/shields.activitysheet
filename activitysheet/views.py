from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import DailyActivitySheet, Activity, Person
from .forms import ActivityForm
from datetime import datetime
import calendar


def index(request):
    # "If there is already a daily activity sheet for today, add to / complete it.  Otherwise create a new daily activity sheet."
    activitysheet = DailyActivitySheet.objects.filter(date=datetime.now()).first()
    if activitysheet:
        activities = activitysheet.activity_set.all()
    else:
        # @TODO change person equal to user after learning django authentication
        activitysheet = DailyActivitySheet(person=Person.objects.get(pk=1), date=datetime.now())
        activitysheet.save()
        activities = {}

    form = ActivityForm()
    context = { 'activities': activities, 'form': form,
                'day_of_week' : calendar.day_name[activitysheet.date.weekday()],
                'activitysheet' : activitysheet }

    return render(request, 'activitysheet/index.html', context)

@require_POST
def addActivity(request, activitysheet_id):

    #post = request.POST.copy()
    #post['start_time'] = convertTime(post['start_time'])
    #post['end_time'] = convertTime(post['end_time'])
    form = ActivityForm(request)

    if form.is_valid():
        new_activity = Activity(
            activitysheet=DailyActivitySheet.objects.get(pk=activitysheet_id),
            name=form.cleaned_data['name'],
            start_time=form.cleaned_data['start_time'],
            end_time=form.cleaned_data['end_time'])
        new_activity.save()

    return redirect('index')

# convertTime accepts a string in the format 1:30 PM and returns a string in format 13:30
def convertTime(time):
	time = datetime.strptime(time, '%I:%M %p')
	return time.strftime('%H:%M')

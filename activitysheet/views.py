from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user

from .models import DailyActivitySheet, Activity
from .forms import ActivityForm
from datetime import datetime
import calendar

def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login')

    # "If there is already a daily activity sheet for today, add to / complete it.  Otherwise create a new daily activity sheet."
    activitysheet = DailyActivitySheet.objects.filter(
    date=datetime.now()).filter(user=get_user(request)).first()
    if activitysheet:
        activities = activitysheet.activity_set.all()
    else:
        activitysheet = DailyActivitySheet(user=get_user(request), date=datetime.now())
        activitysheet.save()
        activities = {}

    form = ActivityForm()
    context = { 'activities': activities, 'form': form,
                'day_of_week' : calendar.day_name[activitysheet.date.weekday()],
                'activitysheet' : activitysheet }

    return render(request, 'activitysheet/index.html', context)

class DailyActivitySheetList(ListView):

    def get_queryset(self):
        self.user = self.request.user
        return DailyActivitySheet.objects.filter(user=self.user)

class ActivityList(ListView):

    def get_queryset(self):
        self.activitysheet = get_object_or_404(DailyActivitySheet, id=self.kwargs['activitysheet_id'])
        return Activity.objects.filter(activitysheet=self.activitysheet)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activitysheet'] = self.activitysheet
        return context

class ActivityUpdate(UpdateView):
    model = Activity
    fields = ['name', 'start_time', 'end_time']
    template_name_suffix = '_update_form'

def deleteActivity(request, pk):
    Activity.objects.get(pk=pk).delete()
    return redirect('index')

@require_POST
def addActivity(request, activitysheet_id):
    post=request.POST.copy()
    post['start_time'] = convertTime(post['start_time'])
    post['end_time'] = convertTime(post['end_time'])

    form = ActivityForm(post)

    if form.is_valid():
        new_activity = Activity(
            activitysheet=DailyActivitySheet.objects.get(pk=activitysheet_id),
            name=form.cleaned_data['name'],
            start_time=form.cleaned_data['start_time'],
            end_time=form.cleaned_data['end_time'])
        new_activity.save()

    return redirect('index')

###################
# function convertTime
# accepts a string in format 01:30 PM and returns a string in format 13:30
# also rounds to the nearest specified MINUTE_INCREMENT
def convertTime(time):
    MINUTE_INCREMENT = 15
    new_time = datetime.strptime(time, '%H:%M')
    hour = new_time.strftime('%H')
    minute = new_time.strftime('%M')
    minute = (round(int(minute) / MINUTE_INCREMENT)*MINUTE_INCREMENT)
    if minute == 60:
        hour = int(hour)+1
        minute = 0
        if hour == 24:
            hour = 0
    return str(hour)+":"+str(minute)

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

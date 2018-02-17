from django.shortcuts import render, redirect, get_object_or_404
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
    init_start = None
    if activities and activities.last().is_complete():
        init_start = activities.last().end_time
    form = None
    if activities and activities.last().is_complete() or not activities:
        form = ActivityForm(initial={
            #'name': init_name,
            'start_time': init_start.strftime('%H:%M') if init_start else None
            #'end_time': init_end.strftime('%H:%M') if init_end else ""
            }
        )
    context = {
        'activities': activities,
        'form': form,
        'day_of_week' : calendar.day_name[activitysheet.date.weekday()],
        'activitysheet' : activitysheet
    }

    return render(request, 'activitysheet/index.html', context)

class DailyActivitySheetList(ListView):

    def get_queryset(self):
        self.user = self.request.user
        return DailyActivitySheet.objects.filter(user=self.user)

class ActivityList(ListView):

    def get_queryset(self):
        self.activitysheet = get_object_or_404(DailyActivitySheet, id=self.kwargs['activitysheet_id'])
        return Activity.objects.filter(activitysheet=self.activitysheet)
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activitysheet'] = self.activitysheet
        return context
"""
class ActivityUpdate(UpdateView):
    form_class = ActivityForm
    model = Activity
    template_name_suffix = '_update_form'
    success_url = '/'
    #def get_queryset(self):
        #return get_object_or_404(Activity, id=self.kwargs['pk'])
        #return Activity.objects.filter(pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity_id'] = self.kwargs['pk']
        print(vars(context['form']['start_time'].field.widget     ))
        return context

    def get_initial(self):
        # Can I just use super().get_initial()?
        initial = super(ActivityUpdate, self).get_initial()

        # retrieve current object
        activity_object = self.get_object()

        initial['start_time']= activity_object.start_time.strftime('%H:%M') if activity_object.start_time else None
        initial['end_time']= activity_object.end_time.strftime('%H:%M') if activity_object.end_time else None
        return initial


def deleteActivity(request, pk):
    Activity.objects.get(pk=pk).delete()
    return redirect('index')


def addActivity(request, activitysheet_id):
    post=request.POST.copy()
    if post['start_time']:
        post['start_time'] = convertTime(post['start_time'])
    if post['end_time']:
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

def updateActivity(request, pk):
    post=request.POST.copy()
    post['start_time']= convertTime(post['start_time']) if post['start_time'] else None
        #post['start_time'] = convertTime(post['start_time'])
    post['end_time']= convertTime(post['end_time']) if post['end_time'] else None
    form = ActivityForm(post)
    if form.is_valid():
        print('form is valid!')
        activity = Activity.objects.get(pk=pk)
        activity.name = form.cleaned_data['name']
        activity.start_time = form.cleaned_data['start_time']
        activity.end_time = form.cleaned_data['end_time']
        activity.save()

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

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, inch, portrait
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
from io import BytesIO

from .models import ActivitySheet, Activity
from .forms import ActivityForm, RegistrationForm
from .secrets import HR_EMAIL
from datetime import datetime, date
import calendar


def index(request):
	if not request.user.is_authenticated:
		return redirect('accounts/login')

	# "If there is already an activity sheet for today,
	# add to / complete it.  Otherwise create a new activity sheet."
	activitysheet = ActivitySheet.objects.filter(
		date=datetime.now()).filter(user=get_user(request)).first()
	if activitysheet:
		activities = activitysheet.activity_set.all()
	else:
		activitysheet = ActivitySheet(user=get_user(request), date=datetime.now())
		activitysheet.save()
		activities = {}
	init_start = None
	if activities and activities.last().is_complete():
		init_start = activities.last().end_time
	form = None
	if activities and activities.last().is_complete() or not activities:
		if not activitysheet.is_complete:
			form = ActivityForm(initial={
				'start_time': init_start.strftime('%H:%M') if init_start else None
				}
			)
	context = {
		'activities': activities,
		'form': form,
		'day_of_week': calendar.day_name[activitysheet.date.weekday()],
		'activitysheet': activitysheet
	}

	return render(request, 'activitysheet/index.html', context)


class ActivitySheetList(ListView):

	def get_queryset(self):
		self.user = self.request.user
		return ActivitySheet.objects.filter(user=self.user).order_by('-date')


class ActivityList(ListView):

	def get_queryset(self):
		self.activitysheet = get_object_or_404(
			ActivitySheet,
			id=self.kwargs['pk']
		)
		return Activity.objects.filter(activitysheet=self.activitysheet)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['activitysheet'] = self.activitysheet
		return context

def generate_pdf(request, activitysheet):
	buffer1 = BytesIO()
	doc = SimpleDocTemplate(
		buffer1,
		pagesize=A4,
		rightMargin=30,leftMargin=30,
		topMargin=30,
		bottomMargin=18
	)
	doc.pagesize = portrait(A4)
	elements = []

	# Generate table data
	data = [['', 'Start Time', 'End Time', 'Total Time']]
	activities = activitysheet.activity_set.all()
	for activity in activities:
		data.append([
			activity.name,
			activity.start_time.strftime('%I:%M %p'),
			activity.end_time.strftime('%I:%M %p'),
			str(activity.total_time) + " hrs"
		])

	#Configure style and word wrap
	style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])

	s = getSampleStyleSheet()
	style_body_text = s["BodyText"]
	style_body_text.wordWrap = 'CJK'
	style_heading = s['Heading1']

	#Build the data
	elements.append(Paragraph(
		"Daily Timesheet - " +
		activitysheet.date.strftime('%x') + " - " +
		calendar.day_name[activitysheet.date.weekday()],
		style_heading
		)
	)
	elements.append(Paragraph(request.user.username, style_heading))
	elements.append(Spacer(0, 0.1*inch))
	data2 = [[Paragraph(cell, style_body_text) for cell in row] for row in data]
	t=Table(data2)
	t.setStyle(style)

	#Send the data and build the file
	elements.append(t)
	elements.append(Spacer(0, 0.1*inch))
	elements.append(Paragraph(str(activitysheet.total_time) + " hours total", style_heading))
	doc.build(elements)

	#p.showPage()
	#p.save()
	pdf = buffer1.getvalue()
	buffer1.close()
	return pdf


def send_pdf(request, activitysheet):
	pdf = generate_pdf(request, activitysheet)
	date = activitysheet.date.strftime('%m-%d-%Y')
	title = 'Timesheet - {} {}'.format(request.user.username, date)
	content = '{} - Total Hours: {}'.format(request.user.username, activitysheet.total_time)
	print("HR_EMAIL: " + HR_EMAIL)
	msg = EmailMessage(title, content, 'webservice@brandonhebel.com', [request.user.email, HR_EMAIL])
	msg.attach('Timesheet_{}_{}.pdf'.format(request.user.username, date), pdf, 'application/pdf')
	msg.content_subtype = "html"
	msg.send()

def complete_activitysheet(request, pk):
	if request.method != 'POST':
		return redirect('index')
	activitysheet = ActivitySheet.objects.get(pk=pk)
	total_time = 0
	for activity in activitysheet.activity_set.all():
		total_time += activity.total_time
	activitysheet.total_time = total_time
	activitysheet.save()
	send_pdf(request, activitysheet)
	activitysheet.is_complete = True
	activitysheet.save()
	return redirect('index')


class ActivityUpdate(UpdateView):
	form_class = ActivityForm
	model = Activity
	template_name_suffix = '_update_form'
	success_url = '/'
	# def get_queryset(self):
		# return get_object_or_404(Activity, id=self.kwargs['pk'])
		# return Activity.objects.filter(pk)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['activity_id'] = self.kwargs['pk']
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
	if request.method != 'POST':
		return redirect('index')
	Activity.objects.get(pk=pk).delete()
	return redirect('index')


def addActivity(request, pk):
	if request.method != 'POST':
		return redirect('index')
	name, start_time, end_time, total_time = add_or_update_activity(request, pk)
	new_activity = Activity(
		activitysheet=ActivitySheet.objects.get(pk=pk),
		name=name,
		start_time=start_time,
		end_time=end_time,
		total_time=total_time
	)
	new_activity.save()
	return redirect('index')


def updateActivity(request, pk):
	if request.method != 'POST':
		return redirect('index')
	name, start_time, end_time, total_time = add_or_update_activity(request, pk)
	activity = Activity.objects.get(pk=pk)
	activity.name = name
	activity.start_time = start_time
	activity.end_time = end_time
	activity.total_time = total_time
	activity.save()
	return redirect('index')

def add_or_update_activity(request, pk):
	post = request.POST.copy()
	post['start_time']= convertTime(post['start_time']) if post['start_time'] else None
	post['end_time']= convertTime(post['end_time']) if post['end_time'] else None
	form = ActivityForm(post)
	if form.is_valid():
		name = form.cleaned_data['name']
		start_time = form.cleaned_data['start_time']
		end_time = form.cleaned_data['end_time']
		total_time = None
		if start_time and end_time:
			total_time = calcHours(start_time, end_time)
	return name, start_time, end_time, total_time


def calcHours(start, end):
	total_time = datetime.combine(date.today(), end) - datetime.combine(date.today(), start)
	return total_time.seconds / 3600
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
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:
		form = RegistrationForm()
	context = {'form': form}
	return render(request, 'registration/register.html', context)


def view_404(request):
	return redirect('index')

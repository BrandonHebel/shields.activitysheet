from django.urls import path
from django.views.generic import ListView
from .views import ActivitySheetList, ActivityList, ActivityUpdate
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('addActivity/<int:pk>', login_required(views.addActivity), name='addActivity'),
	path('register', views.register, name='register'),
	path('viewSheets', login_required(ActivitySheetList.as_view()), name='viewSheets'),
	path('viewActivities/<int:pk>/<int:submitting>', login_required(ActivityList.as_view()), name='viewActivities'),
	path('updateActivityForm/<int:pk>', login_required(ActivityUpdate.as_view()), name="updateActivityForm"),
	path('updateActivity/<int:pk>', login_required(views.updateActivity), name="updateActivity"),
	path('deleteActivity/<int:pk>', login_required(views.deleteActivity), name='deleteActivity'),
	path('complete_activitysheet/<int:pk>', login_required(views.complete_activitysheet), name='complete_activitysheet'),
	path('view_activitysheet_pdf/<int:pk>', login_required(views.view_activitysheet_pdf), name='view_activitysheet_pdf'),

]

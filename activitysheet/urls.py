from django.urls import path
from django.views.generic import ListView
from .views import DailyActivitySheetList, ActivityList, ActivityUpdate

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('addActivity/<activitysheet_id>', views.addActivity, name='addActivity'),
	path('register', views.register, name='register'),
	path('viewSheets', DailyActivitySheetList.as_view(), name='viewSheets'),
	path('viewActivities/<int:activitysheet_id>', ActivityList.as_view(), name='viewActivities'),
	path('updateActivity/<int:pk>', ActivityUpdate.as_view(), name="updateActivity"),
	path('deleteActivity/<int:pk>', views.deleteActivity, name='deleteActivity')
	#path('editActivity', views.ActivityView, name='editActivity')
]

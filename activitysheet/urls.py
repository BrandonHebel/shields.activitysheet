from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('addActivity/<activitysheet_id>', views.addActivity, name='addActivity')
]

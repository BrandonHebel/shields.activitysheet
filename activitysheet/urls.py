from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('addActivity/<activitysheet_id>', views.addActivity, name='addActivity'),
	path('register', views.register, name='register'),
	path('viewSheets', views.viewSheets, name='viewSheets')
]

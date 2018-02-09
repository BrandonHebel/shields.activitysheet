from django.db import models
from django.conf import settings

class DailyActivitySheet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateField()

	def __str__(self):
		return self.date.strftime('%m/%d/%Y')

class Activity(models.Model):
	activitysheet = models.ForeignKey(DailyActivitySheet, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	start_time = models.TimeField()
	end_time = models.TimeField()

	def __str__(self):
		return self.name

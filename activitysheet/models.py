from django.db import models
from django.conf import settings

class DailyActivitySheet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateField()

	def __str__(self):
		return self.date.strftime('%m/%d/%Y')

class Activity(models.Model):
	activitysheet = models.ForeignKey(DailyActivitySheet, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=True)
	start_time = models.TimeField(null=True, blank=True)
	end_time = models.TimeField(null=True, blank=True)

	def __str__(self):
		return self.name

	def is_complete(self):
		return self.name and self.start_time and self.end_time

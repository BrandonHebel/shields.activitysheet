from django.db import models
from django.conf import settings

class ActivitySheet(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateField()
	is_complete = models.BooleanField(default=False)
	total_time = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)

	def __str__(self):
		return '{} {}'.format(self.user.username, self.date.strftime('%m/%d/%Y'))

	def update_total_time(self):
		total_time = 0
		for activity in self.activity_set.all():
			if activity.is_complete():
				total_time += activity.total_time
		self.total_time = total_time
		self.save()

class Activity(models.Model):
	activitysheet = models.ForeignKey(ActivitySheet, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=True)
	start_time = models.TimeField(null=True, blank=True)
	end_time = models.TimeField(null=True, blank=True)
	total_time = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)

	def __str__(self):
		return self.name

	def is_complete(self):
		return self.name and self.start_time and self.end_time

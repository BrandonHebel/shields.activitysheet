from django.db import models

class Person(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class DailyActivitySheet(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
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
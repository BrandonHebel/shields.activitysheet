from django.contrib import admin

from .models import Person, DailyActivitySheet, Activity

admin.site.register(Person)
admin.site.register(DailyActivitySheet)
admin.site.register(Activity)

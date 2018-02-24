from django.contrib import admin

from .models import ActivitySheet, Activity

class ActivityInLine(admin.TabularInline):
    model = Activity

class ActivitySheetAdmin(admin.ModelAdmin):
    fields = ('user', 'date', 'is_complete', 'total_time')
    inlines = [ActivityInLine]

admin.site.register(ActivitySheet, ActivitySheetAdmin)
admin.site.register(Activity)

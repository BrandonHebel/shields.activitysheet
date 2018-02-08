# Generated by Django 2.0.1 on 2018-02-08 04:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitysheet', '0003_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyactivitysheet',
            name='person',
        ),
        migrations.AddField(
            model_name='dailyactivitysheet',
            name='user',
            field=models.ForeignKey(default='', on_delete='CASCADE', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
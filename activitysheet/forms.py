from django import forms
from .models import Activity#, DailyActivitySheet

"""
class ActivityForm(forms.Form):

    name = forms.CharField(label='Name', max_length=30)

    start_time = forms.TimeField(label='Start Time', widget=forms.TimeInput(
        attrs={
            'class': 'timepicker'
        }
    ))

    end_time = forms.TimeField(label='End Time', widget=forms.TimeInput(
        attrs={
            'class': 'timepicker'
        }
    ))
"""
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        widgets = {
            'start_time': forms.TextInput(attrs={'class': 'timepicker', 'autocomplete': 'off'}),
            'end_time': forms.TextInput(attrs={'class': 'timepicker', 'autocomplete': 'off'}),
            'activitysheet': forms.HiddenInput()
        }
"""
class ActivitySheetForm(forms.ModelForm):
	class Meta:
		model = DailyActivitySheet
     	fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'class': 'datepicker'}),
        }
"""
#name = forms.ChoiceField(choices=choices)

from django import forms
from .models import DailyActivitySheet


class ActivityForm(forms.Form):

    name = forms.CharField(label='Name', max_length=30)  # , widget=forms.TextInput(
    # attrs={
    #	'class' : 'form-control'
    #}
    #))

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
class ActivitySheetForm(forms.ModelForm):
	class Meta:
		model = DailyActivitySheet
     	fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'class': 'datepicker'}),
        }
"""
#name = forms.ChoiceField(choices=choices)

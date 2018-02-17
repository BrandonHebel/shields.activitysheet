from django import forms
from .models import Activity#, DailyActivitySheet
"""
class ActivityForm(forms.Form):

    name = forms.CharField(label='Name', max_length=30)

    start_time = forms.TimeField(label='Start Time', widget=forms.TimeInput(
        format='%I:%M %p',
        attrs={
            'autocomplete': 'off',
            'type': 'time'
        }
    ))

    end_time = forms.TimeField(label='End Time', widget=forms.TimeInput(
        format='%I:%M %p',
        attrs={
            'autocomplete': 'off',
            'type': 'time'
        }
    ))
    """
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'start_time', 'end_time']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'required': False,
                }
            ),
            'start_time': forms.TimeInput(
                format='%I:%M %p',
                attrs={
                    'required': False,
                    'autocomplete': 'off',
                    'type': 'time',
                }
            ),
            'end_time': forms.TimeInput(
                format='%I:%M %p',
                attrs={
                    'required': False,
                    'autocomplete': 'off',
                    'type': 'time',
                }
            )
        }
    #def clean_bar(self):
        #return self.cleaned_data['bar'] or None
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

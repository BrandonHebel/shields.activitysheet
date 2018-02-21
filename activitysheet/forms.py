from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Activity

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


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

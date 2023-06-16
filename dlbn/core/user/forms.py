from django import forms
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class LoginForm(AuthenticationForm):
    pass

class ResendVerificationEmailForm(forms.Form):
    email = forms.EmailField()

    widgets = {
        'email': forms.TextInput(attrs={'class': 'form-control'}),
    }
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200,
                             widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                           'placeholder': "Email",
                                                           }))
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                               'placeholder': "First Name"}))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                              "placeholder": "Last Name"}))
    birth_date = forms.DateField(initial=datetime.date.today,
                                 widget=forms.widgets.DateInput(attrs={'type': 'date',
                                                                       'class': "form-control input-lg"}))
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': "form-control input-lg",
                                                             'placeholder': "Username"}))
    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'class': "form-control input-lg",
                                                                  'placeholder': "Password"}))
    password2 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'class': "form-control input-lg",
                                                                  "placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'birth_date', 'password1', 'password2', )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("User already exists.")
        return username


class LoginForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                              'placeholder': "Email",
                                                              }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control input-lg",
                                                                 'placeholder': "Password"}))

    class Meta:
        model = User
        fields = ('email', 'password')

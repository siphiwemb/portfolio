from django import forms
from .models import (Profile, User)
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cellphone', 'house_no', 'street', 'surburb', 'city', 'state', 'latitude', 'longitude')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)


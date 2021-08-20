from django import forms
from .models import (Profile, User)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cellphone', 'house_no', 'street', 'surburb', 'city', 'state', 'latitude', 'longitude')

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')

        try:
            float(latitude)
            return latitude
        except ValueError:
            raise forms.ValidationError("Field only expects decimal values.")


    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')

        try:
            float(longitude)
            return longitude
        except ValueError:
            raise forms.ValidationError("Field only expects decimal values.")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True, widget=forms.PasswordInput)

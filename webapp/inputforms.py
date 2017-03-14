from django.forms import ModelForm
from . import models
from django import forms


class user_form(ModelForm):

     class Meta():
         model = models.user2
         fields = ['us_name', 'us_surname', 'us_role']#, 'us_id']


class delete_user(forms.Form):

    us_id = forms.IntegerField()


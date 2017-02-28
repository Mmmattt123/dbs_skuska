from django.forms import ModelForm
from . import models


class user_form(ModelForm):

     class Meta():
         model = models.user2
         fields = ['us_name', 'us_surname', 'us_role']#, 'us_id']
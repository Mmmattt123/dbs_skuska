from django.forms import ModelForm
from . import models
from django import forms


class company_form(ModelForm):

    class Meta():
        model = models.Company
        fields = ['company_name', 'company_country']


class delete_user(forms.Form):

    us_id = forms.IntegerField()


class next_company(forms.Form):

    next_val = forms.IntegerField()


class find_company(forms.Form):
    
    company_str = forms.CharField()




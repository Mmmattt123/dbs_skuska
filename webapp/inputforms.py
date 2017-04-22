from django.forms import ModelForm
from . import models
from django import forms
from . import form_choises
import datetime

class company_form(ModelForm):
    company_country = forms.ChoiceField(choices=form_choises.COUNTRIES)

    class Meta:
        model = models.Company
        fields = ['company_name', 'company_country']


class delete_user(forms.Form):

    us_id = forms.IntegerField()


class next_company(forms.Form):

    next_val = forms.IntegerField()


class find_company(forms.Form):
    
    company_str = forms.CharField()


class add_manager(ModelForm):
    manager_company_id = forms.IntegerField()
    class Meta:
        model = models.Manager
        fields = ['manager_name', 'manager_surname']

class add_department(ModelForm):

    class Meta:
        model = models.Department
        fields = ['department_name','department_city', 'department_address', 'department_zipcode']

class add_cowork(ModelForm):

    class Meta:
        model = models.working_on
        fields = ['w_company','w_project']
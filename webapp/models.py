from django.db import models
from django.forms import ModelForm

# Create your models here.
class user2(models.Model):

    us_id = models.AutoField(primary_key=True)
    us_name = models.CharField(max_length = 10)
    us_surname = models.CharField(max_length = 15)
    us_role = models.IntegerField()


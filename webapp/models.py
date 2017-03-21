from django.db import models
from django.forms import ModelForm

# Create your models here.
class user2(models.Model):

    us_id = models.AutoField(primary_key=True)
    us_name = models.CharField(max_length = 10)
    us_surname = models.CharField(max_length = 15)
    us_role = models.IntegerField()


# class Company(models.Model):
#
#     id_company = models.AutoField(primary_key=True)
#     company_name = models.CharField(max_length=25)
#     company_country = models.CharField(max_length=25)
#     # company_created_at = models.DateField(auto_created=True)
#
#
# class Manager(models.Model):
#
#     id_manager = models.AutoField(primary_key=True)
#     manager_name = models.CharField(max_length=15)
#     manager_surname = models.CharField(max_length=15)
#     manager_company = models.ForeignKey(Company, on_delete=models.CASCADE)
#
#
# class Project(models.Model):
#
#     id_project = models.AutoField(primary_key=True)
#     project_name = models.CharField(max_length=25)
#     # project_set_at = models.DateField(auto_created=True)
#     project_end_at = models.DateField()
#     project_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
#
#
# class Employee(models.Model):
#
#     id_employee = models.AutoField(max_length=True)
#     employee_name = models.CharField(max_length=15)
#     employee_surname = models.CharField(max_length=15)
#     employee_project = models.ForeignKey(Project, on_delete=models.CASCADE)
#
#
# class Task(models.Model):
#
#     id_task = models.AutoField(primary_key=True)
#     task_name = models.CharField(max_length=25)
#     # task_note = models.CharField(max_length=300)
#     task_end_at = models.DateField()
#     task_project = models.ForeignKey(Project, on_delete=models.CASCADE)
#
# class Milestone(models.Model):
#
#     id_milestone = models.AutoField(primary_key=True)
#     milestone_name = models.CharField(max_length=25)
#     milestone_end_at = models.DateField()
#     milestone_project = models.ForeignKey(Project, on_delete=models.CASCADE)
#
#
# class working_on(models.Model):
#
#     working_on_task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     working_on_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)





from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^insert', views.insert),
	url(r'^delete_company', views.delete),
	url(r'^next_company', views.next_company),
	url(r'^previous_company', views.previous_company),
	url(r'^company_schedule', views.company_schedule),
	url(r'^company_find', views.company_find),
	url(r'add_company', views.add_company),
	url(r'add_manager', views.add_manager),
	url(r'find_cowork_project', views.find_cowork_project),
	url(r'add_cowork', views.add_cowork),
	url(r'add_department', views.add_department),
	url(r'delete_cowork',views.delete_cowork),
	url(r'delete_manager', views.delete_manager),
	url(r'project_shedule',views.project_schedule),
	url(r'update_task',views.update_task),
	url(r'department_schedule',views.department_schedule),
]

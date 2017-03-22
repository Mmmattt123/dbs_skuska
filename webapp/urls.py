from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^insert', views.insert),
	url(r'^delete_user', views.delete),
	url(r'^next_company', views.next_company),
    url(r'^previous_company', views.previous_company),
]
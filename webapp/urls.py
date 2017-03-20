from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^insert', views.insert),
	url(r'^delete_user', views.delete),
<<<<<<< HEAD

=======
>>>>>>> 75eed474ab8a3724166f8070f62621ac8b04c144

]
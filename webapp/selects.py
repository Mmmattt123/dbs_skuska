from . import models


def select_user():

	list = [models.user2(u.us_name, u.us_surname, u.us_role, u.us_id) for u in models.user2.objects.raw('SELECT * FROM public.webapp_user2')]

	return list


def select_user_delete():

    user = models.user2.objects.raw('SELECT ')
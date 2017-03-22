from . import models


def select_company_all(start_num):

    # noinspection SqlNoDataSourceInspection
    list_c = [models.Company(c.id, c.company_name, c.company_country) for c in models.Company.objects.raw('SELECT id, company_name, company_country FROM public.webapp_company WHERE id > %s LIMIT 16', [start_num])]

    return list_c, start_num


def select_user_id():

    user = models.user2.objects.raw('SELECT ')
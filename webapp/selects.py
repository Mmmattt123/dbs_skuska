from . import models


def select_company_all(start_num):

    # noinspection SqlNoDataSourceInspection
    list_c = [models.Company(c.id, c.company_name, c.company_country) for c in models.Company.objects.raw('SELECT id, company_name, company_country FROM public.webapp_company WHERE id > %s LIMIT 16', [start_num])]
    return list_c, start_num


def select_company_one(company_id):

    company = [models.Company(company.id, company.company_name, company.company_country)for company in models.Company.objects.raw('SELECT id, company_name, company_country FROM public.webapp_company WHERE id = %s ', [company_id])]
    return company


def select_user_id():

    user = models.user2.objects.raw('SELECT ')


def select_manager_ten(company_id):

    managers = [models.Manager(m.id, m.manager_name, m.manager_surname)for m in models.Manager.objects.raw('SELECT id, manager_name, manager_surname FROM public.webapp_manager WHERE manager_company_id = %s LIMIT 10 ', [company_id])]
    return managers
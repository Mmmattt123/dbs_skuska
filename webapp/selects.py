from . import models
from django.db import connection
from collections import namedtuple


def select_company_all(start_num):
    # noinspection SqlNoDataSourceInspection
    list_c = [models.Company(c.id, c.company_created_at, c.company_name, c.company_country) for c in
              models.Company.objects.raw(
                  "SELECT id, company_name, company_country, company_created_at FROM public.webapp_company OFFSET %s LIMIT 16",
                  [start_num])]
    return list_c, start_num


def select_company_one(company_id):
    company = [models.Company(c.id, c.company_created_at, c.company_name, c.company_country) for c in
               models.Company.objects.raw(
                   'SELECT id, company_name, company_country, company_created_at FROM public.webapp_company WHERE id = %s ',
                   [company_id])]
    return company


def select_latest_company():
    company = [models.Company(c.id, c.company_created_at, c.company_name, c.company_country) for c in
               models.Company.objects.raw(
                   'SELECT id, company_name, company_country, company_created_at FROM public.webapp_company '
                   'ORDER BY company_created_at DESC LIMIT 4', )]
    return company


def select_manager_ten(company_id):
    managers = [models.Manager(m.id, m.manager_registred_at, m.manager_name, m.manager_surname) for m in
                models.Manager.objects.raw(
                    'SELECT id, manager_name, manager_surname, manager_registred_at FROM public.webapp_manager WHERE manager_company_id = %s',
                    [company_id])]
    return managers


def select_project_find(company_str, num):
    # noinspection SqlNoDataSourceInspection
    with connection.cursor() as cursor:
        cursor.execute(
            """WITH T AS (SELECT DISTINCT webapp_project.id, project_name, company_name, row_number() over() FROM webapp_project LEFT JOIN webapp_manager on webapp_manager.id = project_manager_id LEFT JOIN webapp_company on manager_company_id = webapp_company.id where project_name ILIKE %s || '%%' ORDER BY webapp_project.id) SELECT * FROM T WHERE  %s < row_number LIMIT 100  """,
            [company_str, num])
        list_c = dictfetchall(cursor)
        # print(list_c)
        return list_c


def select_co_working_projects(company_id):
    list_c = [models.Project(p.id, p.project_name, p.project_end_at) for p in models.Project.objects.raw(
        'SELECT DISTINCT webapp_project.id, project_name, project_end_at  FROM public.webapp_project LEFT JOIN webapp_working_on ON webapp_project.id = w_project_id WHERE w_company_id = %s ',
        [company_id])]
    return list_c


def select_departments(company_id):
    list_d = [models.Department(d.id, d.department_name, d.department_city, d.department_address, d.department_zipcode)
              for d in models.Department.objects.raw(
            'SELECT id, department_name, department_city, department_address, department_zipcode FROM public.webapp_department WHERE department_company_id = %s',
            [company_id])]
    return list_d


def dictfetchall(cursor):  # https://docs.djangoproject.com/en/1.11/topics/db/sql/  20. 4. 2017 22:01
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def todo_task(project_id):
    query = "SELECT id, task_name, task_note, task_end_at " \
            "FROM public.webapp_task WHERE " + project_id + "= task_project_id and task_status_id='0'"
    list_task = [models.Task(t.id, t.task_name, t.task_note, t.task_end_at) for t in
                 models.Task.objects.raw(query)]
    return list_task


def in_progress_task(project_id):
    query = "SELECT id, task_name, task_note, task_end_at " \
            "FROM public.webapp_task WHERE " + project_id + "= task_project_id and task_status_id = '1'"
    list_task = [models.Task(t.id, t.task_name, t.task_note, t.task_end_at) for t in
                 models.Task.objects.raw(query)]
    return list_task


def finished_task(project_id):
    query = "SELECT id, task_name, task_note, task_end_at " \
            "FROM public.webapp_task WHERE " + project_id + "= task_project_id and task_status_id = '2'"
    list_task = [models.Task(t.id, t.task_name, t.task_note, t.task_end_at) for t in
                 models.Task.objects.raw(query)]
    return list_task


def select_employee(d_id):
    query = "SELECT id, employee_name, employee_surname FROM webapp_employee where employee_department_id="+d_id+";"
    list_e = [models.Employee(e.id, e.employee_name, e.employee_surname) for e in models.Employee.objects.raw(query)]
    return list_e

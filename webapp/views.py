from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from . import selects, inserts, models, inputforms
import datetime
from django.db import connection, transaction

# import sys

# Create your views here.
DEFAULT_COMPANY_PAGEING_CONST = 17


# logger = logging.getLogger(__name__)


def index(request):
    print("index")
    a, b = selects.select_company_all(0)
    next_form = inputforms.next_company(initial={'next_val': b + DEFAULT_COMPANY_PAGEING_CONST})
    previous_form = inputforms.next_company(initial={'next_val': b})
    print(a[0].company_name)
    return render(request, 'webapp/index.html', {'companies': a, 'form2': inputforms.delete_user(),
                                                 'next_company_id': b, 'next_company_form': next_form,
                                                 'previous_company_form': previous_form,
                                                 'find_company': inputforms.find_company(),
                                                 'add_company': inputforms.company_form(),
                                                 'latest_companies': selects.select_latest_company(),
                                                 'country_analyse': selects.country_company()})


def insert(request):
    if request.POST:
        form = inputforms.user_form(request.POST)

        if form.is_valid():
            form.save()

            # form.cleaned_data()
            # list = []
            # list.append(form.us_name)
            # list.append(form.us_surname)
            # list.append(form.us_role)
            # insert.insert_user(form)

    # a.update(csrf(request))

    return render(request, 'webapp/index.html',
                  {'companies': selects.select_company_all(0), 'form': inputforms.user_form(),
                   'form2': inputforms.delete_user()})


def delete(request):
    print("snazim deletovat")
    if request.GET:
        print("deletujem")
        company_id = request.GET.get('company_for_delete')
        print(company_id)
        company = models.Company.objects.filter(id=company_id)
        company.delete()

    return index(request)


def next_company(request):
    if request.POST:
        form = inputforms.next_company(request.POST)

        if form.is_valid():
            next_val = form.cleaned_data['next_val']

            a, b = selects.select_company_all(next_val)

            next_form = inputforms.next_company(initial={'next_val': b + DEFAULT_COMPANY_PAGEING_CONST})
            previous_form = inputforms.next_company(initial={'next_val': b - DEFAULT_COMPANY_PAGEING_CONST})
    return render(request, 'webapp/index.html', {'companies': a, 'add_company': inputforms.company_form(),
                                                 'latest_companies': selects.select_latest_company(),
                                                 'form2': inputforms.delete_user(),
                                                 'next_company': b, 'next_company_form': next_form,
                                                 'previous_company_form': previous_form})


def previous_company(request):
    if request.POST:
        form = inputforms.next_company(request.POST)

        if form.is_valid():
            next_val = form.cleaned_data['next_val']

            a, b = selects.select_company_all(next_val)

            if ((b - DEFAULT_COMPANY_PAGEING_CONST) >= 0):
                next_form = inputforms.next_company(initial={'next_val': b})
                previous_form = inputforms.next_company(initial={'next_val': b - DEFAULT_COMPANY_PAGEING_CONST})
            else:
                next_form = inputforms.next_company(initial={'next_val': DEFAULT_COMPANY_PAGEING_CONST})
                previous_form = inputforms.next_company(initial={'next_val': 0})
    return render(request, 'webapp/index.html', {'companies': a, 'add_company': inputforms.company_form(),
                                                 'latest_companies': selects.select_latest_company(),
                                                 'form2': inputforms.delete_user(),
                                                 'next_company': b, 'next_company_form': next_form,
                                                 'previous_company_form': previous_form})


def company_schedule(request, **id):
    if id:
        company_id = id['id']
    else:
        company_id = request.GET.get('company_id')
    comp = selects.select_company_one(company_id)
    managers = selects.select_manager_ten(company_id)
    projects = selects.select_co_working_projects(company_id)
    departments = selects.select_departments(company_id)
    # print(managers[0].manager_name)
    return render(request, 'webapp/company_schedule.html',
                  {'company': comp[0], 'managers': managers, 'project': projects,
                   'departments': departments, 'num_of_managers': len(managers),
                   'num_of_departments': len(departments), 'manager_form': inputforms.add_manager,
                   'add_department': inputforms.add_department})


def company_find(request):
    if request.POST:
        form = inputforms.find_company(request.POST)
        print(form + 'daco')
        if form.is_valid():
            company_str = form.changed_data(['company_str'])
            print(company_str)
            comp = selects.select_company_find(company_str)
            b = 16
            next_form = inputforms.next_company(initial={'next_val': b + DEFAULT_COMPANY_PAGEING_CONST})
            previous_form = inputforms.next_company(initial={'next_val': b})
            return render(request, 'webapp/index.html',
                          {'companies': comp, 'form': inputforms.user_form(), 'form2': inputforms.delete_user(),
                           'next_company': b, 'next_company_form': next_form, 'previous_company_form': previous_form})
    print('fail')
    return index(request)


def add_company(request):
    if request.POST:
        form = inputforms.company_form(request.POST)
        company = form.save(commit=False)
        company.company_created_at = datetime.date.today()
        company.save()
        print(company)
    return index(request)


def add_manager(request):
    if request.POST:
        form = inputforms.add_manager(request.POST)
        if form.is_valid():
            manager = form.save(commit=False)
            id_company = form.cleaned_data['manager_company_id']
            company = models.Company.objects.filter(id=id_company)
            manager.manager_company = company[0]
            manager.manager_registred_at = datetime.date.today()
            manager.save()
        return company_schedule(request, id=id_company)


def find_cowork_project(request):
    if request.GET:
        name = request.GET.get('id')
        num = request.GET.get('num_i')
        # print(selects.select_project_find(name))
        # for i in :
        #     pass

        # print(json.dumps(selects.select_project_find(name)))

    return JsonResponse(selects.select_project_find(name, num), safe=False)


def add_cowork(request):
    c_id = request.GET.get('company')
    p_id = request.GET.get('project')
    print(c_id, p_id)
    cowork = models.working_on.objects.create(w_company=models.Company.objects.filter(id=c_id)[0],
                                              w_project=models.Project.objects.filter(id=p_id)[0])

    # cowork.w_project = p_id
    # cowork.w_company = c_id
    # cowork.save()
    return company_schedule(request, id=c_id)


def add_department(request):
    if request.POST:
        form = inputforms.add_department(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            id_company = form.cleaned_data['department_company']
            department.department_company = models.Company.objects.filter(id=id_company)[0]
            department.save()
            print(department)
    return company_schedule(request, id=id_company)


def delete_cowork(request):
    if request.GET:
        p_id = request.GET.get('id_for_delete')
        print(p_id)
        co_work = models.working_on.objects.filter(id=p_id)
        co_work.delete()
        return index(request)


def delete_manager(request):
    if request.GET:
        p_id = request.GET.get('id_for_delete')
        print(p_id)
        manager = models.Manager.objects.filter(id=p_id)
        # c_id = manager.w_company.id
        manager.delete()
        return index(request)


def project_schedule(request, **id):
    if (id):
        p_id=id['id']
    else:
        p_id = request.GET.get('project_id')
    project = models.Project.objects.filter(id=p_id)
    print(selects.todo_task(p_id), selects.in_progress_task(p_id), selects.finished_task(p_id))
    remaining = 100
    done = 0
    if (len(selects.todo_task(p_id)) + len(selects.in_progress_task(p_id)) + len(selects.finished_task(p_id))) :
        done= len(selects.finished_task(p_id)) / (len(selects.todo_task(p_id)) + len(selects.in_progress_task(p_id)) + len(selects.finished_task(p_id))) * 100
        remaining = (1-(len(selects.finished_task(p_id))/(len(selects.todo_task(p_id))+len(selects.in_progress_task(p_id))+len(selects.finished_task(p_id)))))*100
    return render(request, 'webapp/project_view.html',
                      {'add_task': inputforms.add_task,
                       'todo': selects.todo_task(p_id),
                       'in_progress': selects.in_progress_task(p_id),
                       'finished': selects.finished_task(p_id),
                       'project': project[0],
                       'done': done,
                       'remaining':remaining
                       # 'milestones': selects.select_milestone(p_id)
                       #'manager': project.project_manager.manager_name+project.project_manager.manager_surname,
                      # 'Owner':
                      })


def update_task(request):
    if request.GET:
        task_id = request.GET.get('update')
        p_id = request.GET.get('project')
        with connection.cursor() as cursor:
            query = "UPDATE webapp_task SET task_status_id = (task_status_id+1)%3 WHERE id ="+task_id+";"
            cursor.execute(query)

    return project_schedule(request, id=p_id)


def department_schedule(request):
    if request.GET:
        d_id = request.GET.get('department')
        c_id = request.GET.get('company')
        department = models.Department.objects.raw("SELECT id, department_name, department_address, department_company_id, department_zipcode FROM webapp_department WHERE id = %s",[d_id])
        print(department)
        departments = selects.select_departments(c_id)

        return render(request, 'webapp/department_schedule.html',
                      {'department': department,
                       'departments': departments,
                       'employees': selects.select_employee(d_id),
                       'current': d_id,
                       })

@transaction.atomic
def department_merge(request):
    if request.GET:

        nd_id = request.GET.get('new')
        cd_id = request.GET.get('current')
        if nd_id == cd_id:
            return index(request)
        prevd = models.Department.objects.filter(id=cd_id)
        new = models.Department.objects.filter(id = cd_id)
        name = prevd[0].department_name

        connection.cursor().execute("BEGIN; UPDATE webapp_employee SET employee_department_id = "+nd_id+" WHERE employee_department_id ="+cd_id+"; UPDATE webapp_department SET department_name = substring(department_name ||' '||'&'||' "+name+"',0,24 )WHERE id= "+nd_id+";")

        # pre skusobne ucely som nepridal to, ze sa povodne oddelenie vymaze



        # try:
        #     connection.cursor.execute("UPDATE webapp_employee SET employee_department = "+nd_id+" WHERE employee_department="+cd_id+";")
        #     new.department_name += name
        #     new.save()
        # except IntegrityError:
        #     transaction.savepoint_rollback(save_point)
        #     print("roled_Back")
        return index(request)


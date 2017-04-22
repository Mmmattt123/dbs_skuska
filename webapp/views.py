from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from . import selects, inserts, models, inputforms
import datetime
import json

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
                                                 'latest_companies': selects.select_latest_company()})


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
                   'num_of_departments': len(departments), 'manager_form': inputforms.add_manager})


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
    print(c_id,p_id)
    cowork = models.working_on.objects.create(w_company=models.Company.objects.filter(id=c_id)[0], w_project= models.Project.objects.filter(id=p_id)[0])

    # cowork.w_project = p_id
    # cowork.w_company = c_id
    # cowork.save()
    return company_schedule(request, id=c_id)
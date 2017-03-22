from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from . import selects, inserts, models, inputforms

# import sys

# Create your views here.
DEFAULT_COMPANY_PAGEING_CONST =16


def index(request):
    print("index")
    a,b = selects.select_company_all(0)
    next_form = inputforms.next_company(initial={'next_val': b+DEFAULT_COMPANY_PAGEING_CONST})
    previous_form = inputforms.next_company(initial={'next_val': b})

    return render(request, 'webapp/index.html', {'companies': a, 'form': inputforms.user_form(), 'form2': inputforms.delete_user(),
                                                 'next_company_id': b, 'next_company_form': next_form, 'previous_company_form': previous_form})


def insert(request):

    if request.POST:
        form =  inputforms.user_form(request.POST)

        if form.is_valid():
            form.save()

        # form.cleaned_data()
        # list = []
        # list.append(form.us_name)
        # list.append(form.us_surname)
        # list.append(form.us_role)
        # insert.insert_user(form)

    #a.update(csrf(request))

    return render(request, 'webapp/index.html', {'companies': selects.select_company_all(0), 'form': inputforms.user_form(), 'form2': inputforms.delete_user()})


def delete(request):

    if request.POST:
        form = inputforms.delete_user(request.POST)

        if form.is_valid():
            user = models.user2.objects.filter( us_id = form.cleaned_data['us_id'])
            user.delete()

    return render(request, 'webapp/index.html', {'companies': selects.select_company_all(0), 'form': inputforms.user_form(), 'form2': inputforms.delete_user()})


def next_company(request):

    if request.POST:
        form = inputforms.next_company(request.POST)

        if form.is_valid():
            next_val = form.cleaned_data['next_val']

            a,b = selects.select_company_all(next_val)

            next_form = inputforms.next_company(initial={'next_val': b + DEFAULT_COMPANY_PAGEING_CONST})
            previous_form = inputforms.next_company(initial={'next_val': b - DEFAULT_COMPANY_PAGEING_CONST})
    return render(request, 'webapp/index.html', {'companies': a, 'form': inputforms.user_form(), 'form2': inputforms.delete_user(),
                                                 'next_company': b, 'next_company_form': next_form, 'previous_company_form': previous_form})


def previous_company(request):

    if request.POST:
        form = inputforms.next_company(request.POST)

        if form.is_valid():
            next_val = form.cleaned_data['next_val']

            a,b = selects.select_company_all(next_val)

            if ( ( b - DEFAULT_COMPANY_PAGEING_CONST ) >= 0):
                next_form = inputforms.next_company(initial={'next_val': b})
                previous_form = inputforms.next_company(initial={'next_val': b - DEFAULT_COMPANY_PAGEING_CONST})
            else:
                next_form = inputforms.next_company(initial={'next_val': DEFAULT_COMPANY_PAGEING_CONST})
                previous_form = inputforms.next_company(initial={'next_val': 0})
    return render(request, 'webapp/index.html', {'companies': a, 'form': inputforms.user_form(), 'form2': inputforms.delete_user(),
                                                 'next_company': b, 'next_company_form': next_form,'previous_company_form': previous_form})
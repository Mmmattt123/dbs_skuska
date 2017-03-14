from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from . import selects, inserts, models, inputforms

# import sys

# Create your views here.

def index(request):
    print("index")
    return render(request, 'webapp/index.html', {'content': selects.select_user(), 'form': inputforms.user_form(), 'form2': inputforms.delete_user()})

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

    return render(request, 'webapp/index.html', {'content': selects.select_user(), 'form': inputforms.user_form(), 'form2': inputforms.delete_user()})


def delete(request):

    if request.POST:
        form = inputforms.delete_user(request.POST)

        if form.is_valid():
            user = models.user2.objects.filter( us_id = form.cleaned_data['us_id'])
            user.delete()

    return render(request, 'webapp/index.html', {'content': selects.select_user(), 'form': inputforms.user_form(), 'form2': inputforms.delete_user()})
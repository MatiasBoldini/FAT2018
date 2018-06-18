from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import six
from django.utils.dateparse import parse_time


# Create your views here.

def profile(request):
    results = {}
    person = Person.objects.get(user=request.user)
    results['duties'] = person.get_duties()
    if person.user_type == 0:
        print("jubilado")
    elif person.user_type == 1:
        return render(request, 'profile_for_doctor.html', results)
    elif person.user_type == 2:
        return render(request, 'profile_for_teacher.html', results)
    elif person.user_type == 3:
        print("admin")
    else:
        print("hacker")

def load_form_classroom(request):
    results = {}
    results['form'] = ClassRoomForm()
    return render(request, 'profile_for_teacher_parts/new_classroom_form.html', results)

def load_form_classroom_day(request):
    results = {}
    results['form_day'] = ClassDayForm()
    return render(request, 'profile_for_teacher_parts/new_day_form.html', results)

def send_form_classroom(request):
    data = {'name': request.POST.get('name'), 'description': request.POST.get('name'), 'duration': request.POST.get('name')}
    form = ClassRoomForm(initial=data)
    print(form.is_valid())
    if form.is_valid():
        cr = Classroom(data)
        cr.save()
    return HttpResponse(form)

def send_form_classroom_day(request):
    pass
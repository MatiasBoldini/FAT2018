from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.http import HttpResponse, JsonResponse
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
    if request.method == "POST":
        p = Person.objects.get(user=request.user)
        if p.user_type == 2 or 3:
            data = {'name': request.POST.get('name'), 'description': request.POST.get('description'), 'duration': request.POST.get('duration')}
            form = ClassRoomForm(data=data)
            if form.is_valid():
                p.get_duties().delete()
                cr = Classroom(name=data['name'], description=data['description'], duration=data['duration'])
                cr.save()
                em = Enrolment_teacher(person=p, classroom=cr)
                em.save()
            return JsonResponse({"id" : cr.id})
    return redirect(profile)

def send_form_classroom_day(request):
    if request.method == "POST":
        data = {'day': request.POST.get('day'), 'start_hour': request.POST.get('start_hour')}
        form = ClassDayForm(data=data)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            classroom = Classroom.objects.get(id=request.POST.get('id'))
            cd = Classroom_day(day=data['day'], start_hour=data['start_hour'], classroom=classroom)
            cd.save()
        return HttpResponse("well done!")
    return redirect(profile)

def remove_classroom(request):
    Classroom.objects.get(id=request.GET.get('id')).delete()
    return HttpResponse("borrado")
    
def load_classroom_data(request):
    results={}
    classroom = Classroom.objects.get(id=request.GET.get('id'))
    results['form'] = ClassRoomForm(initial={'name':classroom.name, 'description':classroom.description, 'duration':classroom.duration})
    results['modify'] = True
    results['days'] = classroom.get_classroom_days()
    return render(request, 'profile_for_teacher_parts/new_classroom_form.html', results)

def load_classroom_day_data(request):
    results={}
    classroom_day = Classroom_day.objects.get(id=request.GET.get('id'))
    results['form_day'] = ClassDayForm(initial={'day':classroom_day.day, 'start_hour':classroom_day.start_hour})
    return render(request, 'profile_for_teacher_parts/new_day_form.html', results)

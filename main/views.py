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
    person = Person.objects.get(user=request.user)
    results = person.get_duties()
    if person.user_type == 0:
        print("jubilado")
    elif person.user_type == 1:
        return render(request, 'profile_for_doctor.html', results)
    elif person.user_type == 2:
        return render(request, 'profile_for_teacher.html', results)
    elif person.user_type == 3:
        results['retireds'] = Person.objects.filter(user_type=0)
        results['doctors'] = Person.objects.filter(user_type=1)
        results['teachers'] = Person.objects.filter(user_type=2)
        results['classrooms'] = Classroom.objects.all()
        results['appointments'] = Appointment.objects.filter(person__isnull=False, authorized=True)
        results['person_requests'] = Person_request.objects.all()
        results['classroom_requests'] = Classroom_request.objects.all()
        results['enrolment_teacher_requests'] = Enrolment_teacher_request.objects.all()
        results['enrolment_student_requests'] = Enrolment_student_request.objects.all()
        results['work_day_requests'] = Work_day_request.objects.all()
        results['classroom_places'] = Classroom_place.objects.all()
        results['appointment_requests'] = Appointment.objects.filter(person__isnull=False, authorized=False)
        return render(request, 'profile_for_admin.html', results)
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
                p.delete_duties()
                cr = Classroom_request(name=data['name'], description=data['description'], duration=data['duration'], user=p)
                cr.save()
            return JsonResponse({"id" : cr.id})
    return redirect(profile)

def send_form_classroom_day(request):
    if request.method == "POST":
        data = {'day': request.POST.get('day'), 'start_hour': request.POST.get('start_hour')}
        form = ClassDayForm(data=data)
        if form.is_valid():
            classroom = Classroom_request.objects.get(id=request.POST.get('id'))
            cd = Classroom_day_request(day=data['day'], start_hour=data['start_hour'], classroom=classroom)
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

def person_requests(request):
    if request.method == "POST":
        person_id = request.POST.get("id")
        person_request = Person_request.objects.get(id=person_id)
        if int(request.POST.get('approved')):
            new_person = Person(user=person_request.user, user_type=person_request.user_type)
            new_person.save()
        else:
            person_request.user.delete()
        person_request.delete()
    return redirect(profile)

def classroom_requests(request):
    if request.method == "POST":
        classroom_id = request.POST.get("id")
        classroom_place_id = request.POST.get("other_id")
        classroom_request = Classroom_request.objects.get(id=classroom_id)
        classroom_place = Classroom_place.objects.get(id=classroom_place_id)
        classroom_day_requests = Classroom_day_request.objects.filter(classroom=classroom_request)
        if int(request.POST.get('approved')):
            new_classroom = Classroom(name=classroom_request.name, description=classroom_request.description, duration=classroom_request.duration)
            new_classroom.save()
            new_enrolment_teacher, created = Enrolment_teacher.objects.get_or_create(person=classroom_request.teacher)
            new_enrolment_teacher.classroom = new_classroom
            new_enrolment_teacher.save()
            for classroom_day_request in classroom_day_requests:
                new_classroom_day = Classroom_day(classroom=new_classroom, classroom_place=classroom_place, day=classroom_day_request.day, start_hour=classroom_day_request.start_hour)
                new_classroom_day.save()
        classroom_request.delete()
    return redirect(profile)
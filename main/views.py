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

my_objects = {
    "person": Person,
    "classroom": Classroom,
    "appointment": Appointment,
    "enrolment_student": Enrolment_student,
    "enrolment_teacher": Enrolment_teacher
}


def main(request):
    results = {}
    results['parallax'] = True
    return render(request, 'main.html', results)

def profile(request):
    if not request.user.is_authenticated:
        return redirect(my_login)
    person = Person.objects.get(user=request.user)
    results = person.get_duties()
    if person.user_type == 0:
        return render(request, 'profile_for_retired.html', results)
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
        results['work_day_request'] = Work_day_request.objects.all()
        results['appointment_requests'] = Appointment.objects.filter(person__isnull=False, authorized=False)
        results['classroom_places'] = Classroom_place.objects.all()
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
                cr = Classroom_request(name=data['name'], description=data['description'], duration=data['duration'], teacher=p)
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
            new_user = User.objects.create_user(person_request.personal_id, person_request.email, person_request.password)
            new_user.first_name = person_request.first_name
            new_user.last_name = person_request.last_name
            new_user.save()
            new_person = Person(user=new_user, user_type=person_request.user_type)
            new_person.save()
        person_request.delete()
    return redirect(profile)

def classroom_requests(request):
    if request.method == "POST":
        classroom_id = request.POST.get("id")
        classroom_place_id = request.POST.get("other_id")
        classroom_request = Classroom_request.objects.get(id=classroom_id)
        classroom_place = Classroom_place.objects.get(id=classroom_place_id)
        classroom_day_requests = Classroom_day_request.objects.filter(classroom=classroom_request)
        print(classroom_request)
        print(classroom_place)
        if int(request.POST.get('approved')):
            new_classroom = Classroom(name=classroom_request.name, description=classroom_request.description, duration=classroom_request.duration)
            new_classroom.save()
            new_enrolment, created = Enrolment_teacher.objects.get_or_create(person=classroom_request.teacher)
            new_enrolment.classroom = new_classroom
            new_enrolment.save() 
            for classroom_day_request in classroom_day_requests:
                new_classroom_day = Classroom_day(classroom=new_classroom, classroom_place=classroom_place, day=classroom_day_request.day, start_hour=classroom_day_request.start_hour)
                new_classroom_day.save()
        classroom_request.delete()
    return redirect(profile)

def enrolment_teacher_requests(request):
    if request.method == "POST":
        enrolment_teacher_request_id = request.POST.get("id")
        enrolment_teacher_request = Enrolment_teacher_request.objects.get(id=enrolment_teacher_request_id)
        if int(request.POST.get('approved')):
            new_enrolment_teacher_request, created = Enrolment_teacher.objects.get_or_create(person=enrolment_teacher_request.person)
            new_enrolment_teacher_request.classroom = enrolment_teacher_request.classroom
            new_enrolment_teacher_request.save()
        enrolment_teacher_request.delete()
    return redirect(profile)

def enrolment_student_requests(request):
    if request.method == "POST":
        enrolment_student_request_id = request.POST.get("id")
        enrolment_student_request = Enrolment_student_request.objects.get(id=enrolment_student_request_id)
        if int(request.POST.get('approved')):
            new_enrolment_student_request, created = Enrolment_student.objects.get_or_create(person=enrolment_student_request.person, classroom=enrolment_student_request.classroom)
            new_enrolment_student_request.save()
        enrolment_student_request.delete()
    return redirect(profile)

def my_login(request):
    if request.user.is_authenticated:
        return redirect(profile)
    results={}
    if request.method == "POST":
        username = request.POST.get("personal_id")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(profile)
        results['error'] = "Usuario o contraseña incorrectos" 
    return render(request, 'login.html', results)

def my_register(request):
    if request.user.is_authenticated:
        return redirect(profile)
    results={}
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            new_person = Person_request(
                first_name=request.POST.get("first_name"), 
                last_name=request.POST.get("last_name"), 
                personal_id=request.POST.get("username"), 
                password=request.POST.get("password"), 
                email=request.POST.get("email"), 
                user_type=request.POST.get("user_type")
            )
            new_person.save()
            return redirect(main)
    else:
        form = RegistroForm()
    results['form'] = form
    return render(request, 'register.html', results)

def my_logout(request):
    logout(request)
    return redirect(my_login)

def work_day_requests(request):
    if request.method == "POST":
        work_day_request_id = request.POST.get("id")
        work_day_request = Work_day_request.objects.get(id=work_day_request_id)
        if int(request.POST.get('approved')):
            new_work_day = Work_day(doctor=work_day_request.doctor , day=work_day_request.day)
            new_work_day.save()
            finish = toMinutes(work_day_request.finish_hour) 
            turn = toMinutes(work_day_request.interval) + toMinutes(work_day_request.duration)
            start = toMinutes(work_day_request.start_hour) + toMinutes(work_day_request.interval)
            while start < finish:
                if (start + turn) < finish:
                    new_appointment = Appointment(work_day=new_work_day, time_attendance=toTime(start))
                    new_appointment.save()
                start += turn                    
        work_day_request.delete()
    return redirect(profile)

def appointment_requests(request):
    if request.method == "POST":
        appointment_request_id = request.POST.get("id")
        appointment_request = Appointment.objects.get(id=appointment_request_id)
        if int(request.POST.get('approved')):
            appointment_request.authorized = True
        else:
            appointment_request.authorized = False
            appointment_request.person = None
        appointment_request.save()
    return redirect(profile)

def unrolment_student(request):
    if request.method == "POST":
        enrolment_student_id = request.POST.get("id")
        enrolment_student = Enrolment_student.objects.get(id=enrolment_student_id)
        enrolment_student.delete()
    return redirect(profile)

def appointments(request):
    if request.method == "POST":
        appointment_id = request.POST.get("id")
        print(appointment_id)
        appointment = Appointment.objects.get(id=appointment_id)
        person = Person.objects.get(user=request.user)
        appointment.person = person
        appointment.save()
    results = {}
    results['work_days'] = Work_day.objects.filter(day__gte=datetime.datetime.now())
    print(results['work_days'])
    return render(request, 'appointments.html', results)

def classrooms(request):
    person = Person.objects.get(user=request.user)
    if request.method == "POST":
        classroom_id = request.POST.get("id")
        classroom = Classroom.objects.get(id=classroom_id)
        new_enrolment = Enrolment_student_request(classroom=classroom, person=person)
        new_enrolment.save()
        print("DONE \n")
    classrooms = Classroom.objects.all()
    wanted_items = set()
    for classroom in classrooms:
        try:
            Enrolment_student.objects.get(classroom=classroom, person=person)
        except Enrolment_student.DoesNotExist:
            wanted_items.add(classroom.id)
    results = {}
    results['classrooms'] = Classroom.objects.filter(id__in=wanted_items)

    return render(request, 'classrooms.html', results)

def form_work_day(request):
    if request.method == "POST":
        form = WorkDayForm(request.POST)
        if form.is_valid():
            doctor = Person.objects.get(user=request.user)
            new_work_day = Work_day_request(
                start_hour=request.POST.get("start_hour"), 
                finish_hour=request.POST.get("finish_hour"),
                duration=request.POST.get("duration"), 
                interval=request.POST.get("interval"), 
                doctor=doctor, day=request.POST.get("day")
            )
            new_work_day.save()
            return redirect(profile)
    results = {}
    results['form'] = WorkDayForm()
    return render(request, 'profile_for_doctor_parts/form_work_day.html', results)

def delete_object(request):
    if request.method == "POST":
        object_id = request.POST.get("id")
        object_name = request.POST.get("name")
        my_object = my_objects[object_name].objects.get(id=object_id)
        my_object.delete()
    return HttpResponse("OK")

def new_enrolment_classroom(request):
    if request.method == "POST":
        classroom_id = request.POST.get("classroom_id")
        classroom = Classroom.objects.get(id=classroom_id)
        person = Person.objects.get(user=request.user)
        new_enrolment = Enrolment_teacher_request(classroom=classroom, person=person)
        new_enrolment.save()
        return redirect(profile)
    results = {}
    results['classrooms'] = Classroom.objects.all()
    return render(request, 'profile_for_teacher_parts/new_enrolment_classroom.html', results)

def toMinutes(time):
    minute = time.minute
    hours = time.hour
    while hours > 0:
        minute += 60
        hours -= 1
    return minute

def toTime(time):
    minute = time
    hour = 0
    while minute >= 60:
        hour += 1
        minute -= 60
    return datetime.time(hour, minute)
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('profile', profile, name='profile'),
    path('my_login', my_login, name='my_login'),
    path('my_register', my_register, name='my_register'),
    path('my_logout', my_logout, name='my_logout'),
    path('form_classroom', form_classroom, name='form_classroom'),
    path('form_classroom_day', form_classroom_day, name='form_classroom_day'),
    path('load_classroom_data', load_classroom_data, name='load_classroom_data'),
    path('load_classroom_day_data', load_classroom_day_data, name='load_classroom_day_data'),
    path('person_requests', person_requests, name='person_requests'),
    path('classroom_requests', classroom_requests, name='classroom_requests'),
    path('enrolment_teacher_requests', enrolment_teacher_requests, name='enrolment_teacher_requests'),
    path('enrolment_student_requests', enrolment_student_requests, name='enrolment_student_requests'),
    path('work_day_requests', work_day_requests, name='work_day_requests'),
    path('appointment_requests', appointment_requests, name='appointment_requests'),
    path('unrolment_student', unrolment_student, name='unrolment_student'),
    path('appointments', appointments, name='appointments'),
    path('classrooms', classrooms, name='classrooms'),
    path('form_work_day', form_work_day, name='form_work_day'),
    path('delete_object', delete_object, name='delete_object'),
    path('new_enrolment_classroom', new_enrolment_classroom, name='new_enrolment_classroom'),
]
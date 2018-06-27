from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('profile', profile, name='profile'),
    path('my_login', my_login, name='my_login'),
    path('my_register', my_register, name='my_register'),
    path('my_logout', my_logout, name='my_logout'),
    path('load_form_classroom', load_form_classroom, name='load_form_classroom'),
    path('load_form_classroom_day', load_form_classroom_day, name='load_form_classroom_day'),
    path('send_form_classroom', send_form_classroom, name='send_form_classroom'),
    path('send_form_classroom_day', send_form_classroom_day, name='send_form_classroom_day'),
    path('remove_classroom', remove_classroom, name='remove_classroom'),
    path('load_classroom_data', load_classroom_data, name='load_classroom_data'),
    path('load_classroom_day_data', load_classroom_day_data, name='load_classroom_day_data'),
    path('person_requests', person_requests, name='person_requests'),
    path('classroom_requests', classroom_requests, name='classroom_requests'),
    path('enrolment_teacher_requests', enrolment_teacher_requests, name='enrolment_teacher_requests'),
    path('enrolment_student_requests', enrolment_student_requests, name='enrolment_student_requests'),
    path('work_day_requests', work_day_requests, name='work_day_requests'),
    path('appointment_requests', appointment_requests, name='appointment_requests'),
    path('form_work_day', form_work_day, name='form_work_day'),
]
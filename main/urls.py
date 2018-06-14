from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('profile', profile, name='profile'),
    path('load_form_classroom', load_form_classroom, name='load_form_classroom'),
    path('load_form_classroom_day', load_form_classroom_day, name='load_form_classroom_day'),
    path('new_classroom', new_classroom, name='new_classroom'),
]
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('profile', profile, name='profile'),
]
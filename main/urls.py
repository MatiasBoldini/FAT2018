from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('page/<page>', goTo, name="route"),
    path('delete/<object>/<object_id>', delete, name="delete"),
    path('logSystem', logSystem, name="logSystem"),
]
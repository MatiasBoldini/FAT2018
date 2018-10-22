from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('page/<page>', goTo, name="route"),
    path('delete/<object>/<object_id>', delete, name="delete"),
    path('logSystem', logSystem, name="logSystem"),
    path('createModel', createModel, name="create"),
    path('aproveRequest', aproveRequest, name="approve"),
    path('load/<page>/<model_name>/<person_type>', loadData, name="data"),
]
from django.forms import ModelForm
from .models import *
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
import datetime

DAYS_CHOICES = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miercoles'),
    (3, 'Jueves'),
    (4, 'Viernes')
)

USER_TYPE_CHOICES = (
    (0, 'Jubilado'),
    (1, 'Doctor'),
    (2, 'Profesor')
)

class WorkDayForm(forms.Form):
    start_hour = forms.TimeField(label='Hora de inicio')
    finish_hour = forms.TimeField(label='Hora de finalizacion')
    day = forms.DateField(label='Fecha')
    duration = forms.TimeField(label='Duracion de cada turno Aprox.')
    interval = forms.TimeField(label='Intervalo entre turnos')
    


class ClassRoomForm(forms.Form):
    name = forms.CharField(label ='Nombre de la clase', max_length=20)
    description = forms.CharField(label='Descripcion',max_length=256)
    duration = forms.TimeField(label='Duracion de cada clase Aprox.')

class ClassDayForm(forms.Form):
    day = forms.ChoiceField(choices=DAYS_CHOICES, label='Dia')
    start_hour = forms.TimeField(label='Hora de inicio')

    # falta funcion de clean

class RegistroForm(forms.Form):
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    username = forms.IntegerField(label='Documento')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    re_password = forms.CharField(label='Repita la contraseña', widget=forms.PasswordInput())
    email = forms.CharField(label='Correo electronico', required=False)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='Tipo de usuario')

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'El documento ya esta en uso')
        if password != re_password:
            self.add_error('password', 'las contraseñas no coinciden')
    
class LoginForm(forms.Form):
    username = forms.IntegerField(label='Documento')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'Usuario no registrado')

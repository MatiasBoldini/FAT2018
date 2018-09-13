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

def main(request):
    results = {}
    results['parallax'] = True
    return render(request, 'main.html', results)

def goTo(request, page):
    if page == 'profile':
        if User.is_authenticated:
            user = Person.objects.get(user=request.user)
            results = user.get_duties()
            if user.user_type == 0:
                page += '_for_retired'
            elif user.user_type == 1:
                page += '_for_doctor'
            elif user.user_type == 2:
                page += '_for_teacher'
            elif user.user_type == 3:
                page += '_for_admin'
            else:
                return HttpResponse("<H4>Error<H4>")
    else:
        results = {}
    return render(request, '{}.html'.format(page), results)

def delete(request, object, object_id):
    obj = globals()[object].objects.get(id=object_id)
    obj.delete()
    return HttpResponse("1")

def logSystem(request):
    if User.is_authenticated:
        logout(request)
        return goTo(request, 'login')
    else:
        pass

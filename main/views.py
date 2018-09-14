from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from . import models
from django.db.models import Model
from django.http import HttpResponse, JsonResponse

def main(request):
    results = {}
    results['parallax'] = True
    return render(request, 'main.html', results)

def goTo(request, page):
    if page == 'profile':
        if request.user.is_authenticated:
            user = models.Person.objects.get(user=request.user)
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
                return HttpResponse(status=400)
        else:
            return main(request)    
    else:
        results = {}
    return render(request, '{}.html'.format(page), results)

def delete(request, object, object_id):
    model = getModel(object)
    if model:
        obj = model.objects.get(id=object_id)
        obj.delete()
        return HttpResponse("1")
    else: 
        return HttpResponse(status=400)

def logSystem(request):
    if request.method == "POST":
        username = request.POST.get("personal_id")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return main(request)
    logout(request)
    return goTo(request, 'login')

def createModel(request):
    if request.method == "POST":
        model = getModel(request.POST['model'])
        if model:
            dic ={}
            for a in request.POST.keys():
                if hasattr(model, a):
                    dic[a]=request.POST[a]
            model.objects.create(**dic)
        else:
            return HttpResponse(status=400)
    return HttpResponse(model)

def aproveRequest(request):
    if request.method == "POST":
        request_id = request.POST['model_id']
        model = getModel(request.POST['model'])
        if model:
            request_obj = model.objects.get(id=request_id)
            request_obj.approved()
            return HttpResponse("1")
    return HttpResponse(status=405)

def getModel(model_name):
    if hasattr(models, model_name):
        model = getattr(models, model_name)
        if issubclass(model, Model):
            return model
    return 0
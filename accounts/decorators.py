from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request , *args,**kwargs):
        if request.user.is_authenticated:
            return redirect ('home')
        else:
            return view_func(request , *args,**kwargs)
    return wrapper_func

def unauthenticated_patient(view_func):
    def wrapper_func(request , *args,**kwargs):
        if request.user.is_authenticated:
            return redirect ('Patienthome')
        else:
            return view_func(request , *args,**kwargs)
    return wrapper_func

def unauthenticated_doctor(view_func):
    def wrapper_func(request , *args,**kwargs):
        if request.user.is_authenticated:
            return redirect ('Doctorhome')
        else:
            return view_func(request , *args,**kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request , *args,**kwargs):
            group = None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args,**kwargs)
            else:
                return redirect ('NotAllowedUsers')
                #return HttpResponse('You are not authorized to view this page')

        return wrapper_func
    return decorator

def Doctor_Only(view_func):

    def wrapper_func(request , *args,**kwargs):
        group = None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name

        if group == 'Patients':
            return redirect('Patienthome')
        else:
            return view_func(request, *args,**kwargs)

    return wrapper_func

def Patient_Only(view_func):

    def wrapper_func(request , *args,**kwargs):
        group = None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name

        if group == 'Doctors':
            return redirect('Doctorhome')
        else:
            return view_func(request, *args,**kwargs)

    return wrapper_func

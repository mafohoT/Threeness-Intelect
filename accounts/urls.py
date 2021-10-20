"""System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('Patienthome/',views.Patienthome ,name='Patienthome'),
    path('login/',views.Login ,name='login'),
    path('Test/',views.Test ,name='Test'),
    path('logout/',views.logout ,name='logout'),
    path('PatientRegister/',views.PatientRegister, name="PatientRegister"),
    path('DoctorRegister/',views.DoctorRegister, name="DoctorRegister"),
    path('Doctorhome/',views.Doctorhome ,name='Doctorhome'),
    path('Adminhome/',views.Adminhome ,name='Adminhome'),
    path('createAppointment/',views.PatientAppointment, name="createAppointment"),
    path('NotAllowedUsers/',views.NotAllowedUsers, name="NotAllowedUsers"),
    path('Doctoravailability/',views.Doctoravailability, name="Doctoravailability"),
    path('delete_patient(P<int:pid>)',views.DeletePatient, name="delete_patient"),
    path('delete_appointment(P<int:pid>)',views.AdminDeleteAppointment, name="delete_appointment"),
    path('Doc_delete_appointment(P<int:pid>)',views.DocDeleteAppointment, name="Doc_delete_appointment"),
    path('updateAppointment(P<int:pid>)',views.updateAppointment, name="updateAppointment"),
    path('ViewAppointment(P<int:pid>)',views.ViewAppointment, name="ViewAppointment"),
    path('SeachPatient',views.SeachPatient, name="SeachPatient"),


]

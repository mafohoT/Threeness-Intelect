from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from . models import Patient,Appointment,DoctorAvailability
from django.db import transaction
from django.forms import ModelForm
#user = User.objects.get()

class CreatePatientForm(UserCreationForm):
    #phonenumber =PhoneNumberField(widget =PhoneNumberPrefixWidget())
    phonenumber = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    #email = forms.EmailField()
    id_number = forms.CharField(required=True)

    class Meta:
        model = User
        #fields = ['username','email','password1','password2','phonenumber','id_number']
        fields = ['username','password1','password2','phonenumber','id_number']

class CreateDoctorForm(UserCreationForm):
    phonenumber =PhoneNumberField(widget =PhoneNumberPrefixWidget())
    username = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    control_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2','phonenumber','control_number']

class CreatePatientAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor','status','appointment_date']

class DoctorAvailabilityForm(ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'

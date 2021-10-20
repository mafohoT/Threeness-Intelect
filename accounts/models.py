from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import rsaidnumber
from django.core.validators import RegexValidator
from datetime import datetime

# Create your models here.
#class User(AbstractUser):
#    appointment_date = models.DateField(auto_now_add=False,null=True)
#    appointment_reason = models.CharField(max_length=200,null=True)

class Admin(models.Model):
    user = models.OneToOneField(User,null = True, on_delete =models.CASCADE)
    username  =models.CharField(max_length=20,null=True)
    id_number  =models.CharField(max_length=13,null=True)
    phonenumber =PhoneNumberField(null=True)
    name = models.CharField(max_length=200,null=True)
    employeenumber = models.CharField(max_length=200,null=True,unique=True)
    def __str__(self):
        return '%s_%s' % (self.username,self.employeenumber)

class Patient(models.Model):
    user = models.OneToOneField(User,null = True, on_delete =models.CASCADE)
    username  =models.CharField(max_length=20,null=True)
    id_number  =models.CharField(max_length=13,null=True)
    phonenumber =PhoneNumberField(null=True)
    name = models.CharField(max_length=200,null=True)
    #surname = models.CharField(max_length=200,null=True)
    appointment_reason = models.CharField(max_length=200,null=True)
    #doctor = models.ForeignKey(Doctor,null = True, on_delete=models.CASCADE)
    appointment_date = models.DateField(auto_now_add=False,null=True)
    def __str__(self):
        return '%s' % (self.username)

class Doctor(models.Model):
    user = models.OneToOneField(User,null = True, on_delete =models.CASCADE)
    username  =models.CharField(max_length=20,null=True)
    control_number  =models.CharField(max_length=20,null=True)
    phonenumber =PhoneNumberField(null=True)
    specialization = models.CharField(max_length=200,null=True)
    def __str__(self):
        return '%s-%s'  % (self.username , self.specialization)
"""
class Specialization(models.Model):
    APPOINTMENT_SPECIALIST = (
                ('Flu' ,'Flu'),
                ('Diabetes','Diabetes'),
                ('Corona_virus','Corona_virus'),
                )
    #name = models.CharField(max_length=200,null=True)
    added_date = models.DateTimeField(auto_now_add=True,null=True)
    specialization = models.CharField(max_length=200,null=True,choices = APPOINTMENT_SPECIALIST)
    def __str__(self):
        return '%s' % (self.specialization)
"""
class Appointment(models.Model):
    STATUS = (
                ('Pending' ,'Pending'),
                ('Checking for available time','Checking for available time'),
                ('Resolved','Resolved'),
                )
    name = models.CharField(max_length=200,null=True)
    appointment_reason = models.CharField(max_length=200,null=True)
    patient = models.ForeignKey(Patient,null = True, on_delete=models.CASCADE,unique = False)
    doctor = models.ForeignKey(Doctor,null = True, on_delete=models.CASCADE,unique = False)
    appointment_date = models.DateField(auto_now_add=False,null=True)
    status = models.CharField(max_length=200,null=True,choices = STATUS)
    id_number  =models.CharField(max_length=13,null=True)
    def __str__(self):
        return'%s_%s' % (self.name ,self.appointment_date)

class DoctorAvailability(models.Model):
    name = models.CharField(max_length=200,null=True)
    doctor = models.ForeignKey(Doctor,null = True, on_delete=models.CASCADE)
    availability_datetime = models.DateTimeField(auto_now_add=False,null=True)
    def __str__(self):
        return'%s_%s' % (self.name ,self.availability_datetime)

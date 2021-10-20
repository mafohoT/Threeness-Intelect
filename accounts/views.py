from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . form import CreatePatientForm,CreateDoctorForm,CreatePatientAppointmentForm,DoctorAvailabilityForm
from . models import Patient,Doctor,Appointment,DoctorAvailability,Admin
from . decorators import unauthenticated_patient,unauthenticated_user,allowed_users,unauthenticated_doctor,Doctor_Only,Patient_Only
from django.contrib.auth.models import User
import phonenumbers
from datetime import datetime
# Create your views here.
#@unauthenticated_patient
def is_valid(number,country):
    try:
        pn = phonenumbers.parse(number,country)
        if phonenumbers.is_possible_number(pn) and phonenumbers.is_valid_number(pn):
            return True
    except phonenumbers.NumberParseException as e:
        return False
    return False
def dateTryParse(date):
    result = True
    formatStr = '%m/%d/%Y'
    try:
        datetime.strptime(date,formatStr)
    except:
        result = False
    return result
def hasValidDate(id):
    year = id[0:2]
    month = id[2:4]
    day = id[4:6]
    date1 = f'{month}/{day}/19{year}'
    date2 = f'{month}/{day}/20{year}'
    return dateTryParse(date1) or dateTryParse(date2)
def isValidNumberWith13Digits(id):
    return len(id)==13 and id.isdigit()
def isOdd(number):
    return number % 2  != 0
def validateSAID(id):
    result = False
    if (isValidNumberWith13Digits(id) and hasValidDate(id)):
        sum = 0
        for idx,char in enumerate(reversed(id)):
            digit = int(char)
            if isOdd(idx):
                digit = digit * 2
                if digit > 9:
                    subSum = 0
                    while digit > 0:
                        subSum += digit % 10
                        digit = digit // 10
                    digit = subSum
            sum += digit
        result = sum % 10 == 0
    return result
def Test(request):
    if request.method == 'POST':
        phone =phonenumbers.parse(request.POST.get('phonenumber'))
        if phonenumbers.is_valid_number(phone) == False:
            messages.error(request,'Check your id number')
        else:
            messages.error(request,'Check your id number')
    return render(request , 'Test.html')
def PatientRegister(request):
    form = CreatePatientForm()
    if request.method == 'POST':
        form = CreatePatientForm(request.POST)
        p = request.POST.get('phonenumber')
        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request,'username already exists,please choose another one')
        elif request.POST.get('password1') != request.POST.get('password2'):
            messages.error(request,'Passwords not matching')
        elif validateSAID(request.POST.get('id_number')) == False:
            messages.error(request,'invalid id number')
        elif is_valid(request.POST.get('phonenumber'),"ZA") == False:
            messages.error(request,'please enter valid South African phone number')
        elif Patient.objects.filter(phonenumber=request.POST.get('phonenumber')).exists():
            messages.error(request,'phone number already exists')
        elif Patient.objects.filter(id_number=request.POST.get('id_number')).exists():
            messages.error(request,'user with identity number -' + request.POST.get('id_number') + ' -already exists')
        else:
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                patient = Patient.objects.create(user=user)
                patient.username = form.cleaned_data["username"]
                #patient.email = form.cleaned_data["email"]
                patient.id_number = form.cleaned_data["id_number"]
                patient.phonenumber = form.cleaned_data["phonenumber"]
                patient.save()
                group = Group.objects.get(name='Patients')
                user.groups.add(group)
                messages.success(request, 'created for : ' + username)
                return redirect('login')
    context = {'form':form}
    return render(request , 'PatientRegistration.html',context)
#@unauthenticated_doctor
def DoctorRegister(request):
    form = CreateDoctorForm()
    if request.method == 'POST':
        form = CreateDoctorForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            doctor = Doctor.objects.create(user=user)
            doctor.username = form.cleaned_data["username"]
            doctor.email = form.cleaned_data["email"]
            doctor.control_number = form.cleaned_data["control_number"]
            doctor.phonenumber = form.cleaned_data["phonenumber"]
            doctor.save()
            group = Group.objects.get(name='Doctors')
            user.groups.add(group)
            messages.success(request, 'created for : ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request , 'DoctorRegistration.html',context)

#@allowed_users(allowed_roles=['Patients'])
#@unauthenticated_patient
def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            login(request,user)
            g = None
            a = None

            if user.groups.exists():
                g= user.groups.all()[0].name
            if g == 'Doctors':
                return redirect('Doctorhome')
            elif g == 'Patients':
                return redirect('Patienthome')
            elif g == 'Admins':
                return redirect('Adminhome')
        else:
            messages.error(request,'username or password incorrect')
    form = AuthenticationForm()
    context = {'form':form}
    return render (request , 'Login.html',context)
from django.contrib.auth import logout as django_logout
#@login_required(login_url='login')
def logout(request):
    django_logout(request)
    return redirect('login')
from django.db.models import Q
@login_required(login_url='login')
#@Doctor_Only
#@allowed_users(allowed_roles=['Doctor'])
def Doctorhome(request):
    searched = None
    if request.method == 'POST':
        searched =request.POST.get('searched')
        if not Appointment.objects.filter(id_number__contains=searched).exists():
            messages.error(request,' user id number does not exist')
        else:
            p = Appointment.objects.filter(id_number__contains=searched)
            context = {'se':searched,'pe':p}
            return render (request,'searched.html',context)
    current_doc = request.user.doctor
    appointment_counts = Appointment.objects.filter(doctor=current_doc,status='Checking for available time').count() + Appointment.objects.filter(doctor=current_doc,status='Pending').count()
    Resolved = Appointment.objects.filter(doctor=current_doc,status='Resolved').count()
    appointment = Appointment.objects.filter(Q(doctor=current_doc,status='Checking for available time') | Q(doctor=current_doc,status='Pending'))
    patientCount = Patient.objects.all().count()
    availability = DoctorAvailability.objects.filter(doctor=current_doc)
    total_patient = Patient.objects.filter().count()
    context = {'num_patient':patientCount,'appointment':appointment,'appointmentscount':appointment_counts,'DoctorAvailability':availability,'Resolv':Resolved}
    return render (request , 'Doctorhome.html',context)
#@login_required(login_url='login')
def Patienthome(request):
    current_user = request.user.patient
    appointment = Appointment.objects.filter(patient=current_user.id)
    all = appointment.filter(status='Resolved')
    pending = appointment.filter(status='Pending').count() + appointment.filter(status='Checking for available time').count()
    total_app = appointment.count()
    resolved = appointment.filter(status='Resolved').count()
    Allpending = appointment.filter(status='Pending')

    context = {'appointments':total_app,'apps':all,'pendingcount':pending,'res':resolved,'Allpendings':Allpending}
    return render (request , 'Patienthome.html',context)

def Adminhome(request):
    appointment_counts = Appointment.objects.all().count()
    appointment = Appointment.objects.all()
    patient = Patient.objects.all()
    patientCount = Patient.objects.all().count()
    availability = DoctorAvailability.objects.all()
    context = {'patients':patient,'num_patient':patientCount,'appointment':appointment,'appointmentscount':appointment_counts,'DoctorAvailability':availability}
    return render(request,'AdminHome.html',context)
#@Patient_Only
from django.forms import inlineformset_factory
@login_required(login_url='login')
def PatientAppointment(request):
    #form = CreatePatientAppointmentForm()
    ini = 'Pending'
    #pending = appointment.filter(status='Pending')
    if request.method == 'POST':
        current_user = request.user.patient
        appointment = Appointment.objects.filter(patient=current_user.id)
        #all = appointment.all()
        p=request.user.patient
        if appointment.filter(status ='Pending') or appointment.filter(status ='Checking for available time'):
            messages.success(request, 'Sorry, you can only have one appointment, you have to first see a doctor with first appointment then you can create a new one!!!')
        else:
            #username = request.POST.get('name')
            reason = request.POST.get('appointment_reason')
            date = request.POST.get('appointment_date')
            patt = request.user.patient
            idnum = request.user.patient.id_number
            Appointment.objects.create(patient = patt,id_number=idnum, name = username,appointment_reason = reason,appointment_date = date,status=ini)
            messages.success(request, 'appointment sent to admin for : ' + request.user.patient + ' You will get alert on the time you can avil yourself')
            return redirect('Patienthome')
        ##form = CreatePatientAppointmentForm()
    context = {}
    return render(request , 'createAppointment.html',context)

#@Doctor_Only
def Doctoravailability(request):
    form = DoctorAvailabilityForm()
    if request.method == 'POST':
            availability = request.POST.get('availability_datetime')
            doc = request.user.doctor
            DoctorAvailability.objects.create(name=request.user.doctor,doctor=request.user.doctor,availability_datetime=availability)
            #patient.save()
            messages.success(request, ' availability time sent to admin. they will send you list of patient once accepted')
            return redirect('Doctorhome')
    context = {'form':form}
    return render(request , 'DoctorAvailability.html',context)

def updateAppointment(request,pid):
    apps = Appointment.objects.get(id=pid)
    form = CreatePatientAppointmentForm(instance=apps)
    if request.method == 'POST':
        form = CreatePatientAppointmentForm(request.POST,instance=apps)
        if form.is_valid():
            form.save()
            return redirect('Adminhome')
    context = {'form':form}
    return render (request,'updateAppointment.html',context)

def SeachPatient(request):
    #appointment = []
    searched = None
    if request.method == 'POST':
        searched =request.POST.get('searched')
        p = Appointment.objects.filter(id_number__contains=searched)
        #return redirect('SeachPatient')
        context = {'se':searched,'pe':p}
        return render (request,'searched.html',context)
    else:
        return render (request,'searched.html',{})

def ViewAppointment(request,pid):
    apps =  Appointment.objects.filter(id=pid)
    #user = request.user.patient
    p = Patient.objects.all()
    context = {'app':apps,'pe':p}
    return render (request,'ViewAppointment.html',context)

def AdminDeleteAppointment(request,pid):
    p = Appointment.objects.get(id=pid)
    p.delete()
    return redirect('Adminhome')

def DocDeleteAppointment(request,pid):
    p = Appointment.objects.get(id=pid)
    p.delete()
    return redirect('Doctorhome')

def DeletePatient(request,pid):
    p = User.objects.get(id=pid)
    p.delete()
    return redirect('Adminhome')

def NotAllowedUsers(request):
    context = {}
    return render(request , 'notauthorized.html',context)

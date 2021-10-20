from django.contrib import admin
from . models import Patient,Doctor,Appointment,DoctorAvailability,Admin
# Register your models here.
#admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
#admin.site.register(Specialization)
admin.site.register(DoctorAvailability)
admin.site.register(Admin)

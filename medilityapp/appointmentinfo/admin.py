from django.contrib import admin
from .models import Appointment, AppointmentDetail, AppointmentPatientListInfo
# Register your models here.

admin.site.register(Appointment)
admin.site.register(AppointmentDetail)
admin.site.register(AppointmentPatientListInfo)


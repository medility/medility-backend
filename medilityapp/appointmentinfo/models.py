from django.db import models
from accounts.models import AddressList, User
from medicalcenter.models import MedicalCentre
from labtest.models import LabTest
from package.models import Package
from timeslot.models import NurseSlot

# Create your models here.
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=200)
    address = models.ForeignKey(AddressList, on_delete=models.CASCADE)
    time_slot = models.CharField(max_length=100)
    date_slot = models.CharField(max_length=100) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    status = models.IntegerField(default=0)
    slotID = models.ForeignKey(NurseSlot, on_delete=models.CASCADE, default=1)


    # def __str__(self) -> str:
    #     return self.appointment_id

class AppointmentDetail(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='appointment', on_delete=models.CASCADE)
    medical_center = models.ForeignKey(MedicalCentre, related_name='center', on_delete=models.CASCADE)
    test_type = models.IntegerField()
    labtest = models.ForeignKey(LabTest, related_name='labtest_info', on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey(Package, related_name='package_info', on_delete=models.CASCADE, null=True, blank=True) 

    # def __str__(self) -> str:
    #     return self.appointment.appointment_id

class AppointmentPatientListInfo(models.Model):
    appointment_detail = models.ForeignKey(AppointmentDetail, related_name='appnt_detail', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return self.appointment_detail
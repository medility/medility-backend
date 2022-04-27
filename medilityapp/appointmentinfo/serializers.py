from rest_framework import serializers
from .models import Appointment, AppointmentDetail,AppointmentPatientListInfo
from labtest.serializers import LabTestSerializer
from accounts.models import AddressList, User
from accounts.serializers import AddressInfoForUserToNurseSerializer, UserSerializer
from labtest.models import LabTest
from medicalcenter.models import MedicalCentre
from medicalcenter.serializers import MedicalCetreSerializer
from package.models import Package
from package.serializers import PackageSerializer
from accounts.models import User
import calendar, time

class AppointmentPatientListInfoSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(User.objects.all(), source='user')

    class Meta:
        model = AppointmentPatientListInfo
        fields = ['id', 'appointment_detail', 'user_detail']


class AppointmentPatientCreateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AppointmentPatientListInfo
        fields = '__all__'


class AppointmentDetailSerializer(serializers.ModelSerializer):
    appnt_detail = AppointmentPatientListInfoSerializer(many=True)
    labtest_detail = LabTestSerializer(LabTest.objects.all(), source='labtest')
    medicalcenter_detail = MedicalCetreSerializer(MedicalCentre.objects.all(), source='medical_center')
    package_detail = PackageSerializer(Package.objects.all(), source='package')

    class Meta:
        model = AppointmentDetail
        fields = ['id', 'medicalcenter_detail', 'test_type', 'package_detail', 'appnt_detail', 'labtest_detail']


class AppointmentDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentDetail
        fields = '__all__'



class AppointmentSerializer(serializers.ModelSerializer):
    appointment = AppointmentDetailSerializer(many=True)
    address_detail = AddressInfoForUserToNurseSerializer(AddressList.objects.all(), source='address')

    class Meta:
        model = Appointment
        fields = ['id', 'appointment_id', 'time_slot', 'date_slot', 'slotID', 'address_detail', 'appointment']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Appointment
        fields = ['id', 'address', 'time_slot', 'date_slot', 'user', 'slotID']

    def create(self, validated_data):
        print(validated_data)
        appointment = Appointment.objects.create(**validated_data)
        appointment.appointment_id = calendar.timegm(time.gmtime())
        appointment.save()
        return appointment



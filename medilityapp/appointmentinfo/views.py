from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from knox.auth import TokenAuthentication
from accounts.models import User
from timeslot.models import NurseSlot
from nurse.models import Nurse
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Appointment, AppointmentDetail, AppointmentPatientListInfo
from .serializers import AppointmentSerializer, AppointmentDetailSerializer, AppointmentPatientListInfoSerializer, AppointmentCreateSerializer, AppointmentDetailCreateSerializer, AppointmentPatientCreateSerializer

# Create your views here.


class AppointmentView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        return Appointment.objects.filter(user=self.request.user, status=status)


class AppointmentCreateView(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    serializer_class = AppointmentCreateSerializer
    queryset = Appointment.objects.all()

    def createAppointment(self, req_data):
        print('inside createappointment')
        print(req_data)
        appointment = AppointmentCreateSerializer(data=req_data)
        if appointment.is_valid():
            appointment.save()
            self.createAppointmentDetail(req_data, appointment.data['id'])
            self.updateNurseSlot(appointment.data['slotID'])
        if appointment.errors:
            return Response(appointment.errors)

    
    def updateAppointment(self, req_data, appointment_id):
        appnt_id = Appointment.objects.get(appointment_id=appointment_id)
        appnt_detail_list = AppointmentDetail.objects.filter(appointment=appnt_id)
        appnt_patient_list = AppointmentPatientListInfo.objects.filter(appointment_detail__in=appnt_detail_list).delete()
        appnt_detail_list.delete()
        self.createAppointmentDetail(req_data, appnt_id.id)

    def createAppointmentDetail(self, req_data, appointment_id):
        print(appointment_id)
        appointment_detail = req_data['appointment']
        for appnt in appointment_detail:
            appnt.update({'appointment': appointment_id})
            appnt_detail = AppointmentDetailCreateSerializer(data=appnt)
            if appnt_detail.is_valid():
                appnt_detail.save()
                self.createAppointmentPatientInfo(
                    appnt['patients'], appnt_detail.data['id'])
            if appnt_detail.errors:
                return Response(appnt_detail.errors)
        return appnt_detail.data['id']

    def createAppointmentPatientInfo(self, patientsInfo, appnt_detail_id):
        for patient in patientsInfo:
            patient_info = {'appointment_detail': appnt_detail_id,
                            'user': User.objects.get(phone=patient['phone']).pk}
            patient_serializer = AppointmentPatientCreateSerializer(
                data=patient_info)
            if patient_serializer.is_valid():
                patient_serializer.save()
            if patient_serializer.errors:
                return Response(patient_serializer.errors)

    def updateNurseSlot(self, slotId):
        nurseSlot = NurseSlot.objects.get(id=slotId)
        nurseSlot.status = 1
        nurseSlot.save()

    def create(self, request, *args, **kwargs):
        req_data = request.data
        appointment_id = req_data.get('appointment_id', None)
        print(request.data)
        req_data.update({"user": self.request.user.pk})
        if not appointment_id:
            self.createAppointment(req_data)
            return Response({'msg': 'created'})
        else:
            self.updateAppointment(req_data, appointment_id)
            return Response({'msg': 'updted'})


class AppointmentByNurseView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    serializer_class = AppointmentSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        dateToFind = self.request.query_params.get('date')
        nurse = Nurse.objects.get(user=self.request.user)
        if dateToFind:
            nurseAppnt = NurseSlot.objects.filter(nurse=nurse, status=1, date_slot__slot_date=dateToFind)
        else:
            nurseAppnt = NurseSlot.objects.filter(nurse=nurse, status=1)
        slotList = []
        for slotId in nurseAppnt:
            slotList.append(slotId.id)
        return Appointment.objects.filter(slotID__in=nurseAppnt, status=status)
from django.shortcuts import render
from rest_framework import generics
from .models import MedicalCentre
from .serializers import MedicalCetreSerializer, \
                        MedicalCetreSerializerById
# Create your views here.


class Center(generics.ListAPIView):
    serializer_class = MedicalCetreSerializer
    queryset = MedicalCentre.objects.all()

class CenterById(generics.RetrieveAPIView):
    serializer_class = MedicalCetreSerializerById
    queryset = MedicalCentre.objects.all()
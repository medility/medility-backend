from rest_framework import serializers
from .models import MedicalCentre
from labtest.serializers import LabTestSerializer
from package.serializers import PackageSerializer

class MedicalCetreSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalCentre
        fields = '__all__'


class MedicalCetreSerializerById(serializers.ModelSerializer):
    tests = LabTestSerializer(many=True)
    package = PackageSerializer(many=True)

    class Meta:
        model = MedicalCentre
        fields = ['id', 'name', 'address', 'pincode', 'tests', 'package']
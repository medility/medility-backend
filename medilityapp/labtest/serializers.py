from .models import LabTest, MedicalCentre
# from medicalcenter.serializers import MedicalCetreSerializer
from rest_framework import serializers


class LabTestSerializer(serializers.ModelSerializer):
    medical_center = serializers.SlugRelatedField(
        read_only=True, slug_field='id', source='medical_centre')
    medical_center_name = serializers.SlugRelatedField(
        read_only=True, slug_field='name', source='medical_centre')
    medical_center_address = serializers.SlugRelatedField(
        read_only=True, slug_field='address', source='medical_centre')
    medical_center_pincode = serializers.SlugRelatedField(
        read_only=True, slug_field='pincode', source='medical_centre')

    class Meta:
        model = LabTest
        fields = ['id', 'name', 'price', 'overview',
                  'instruction', 'medical_center_name', 'medical_center_address', 'medical_center_pincode', 'medical_center']

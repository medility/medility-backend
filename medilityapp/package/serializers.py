from .models import Package, PackageDetail
from rest_framework import serializers


class PackageSerializer(serializers.ModelSerializer):
    
    medical_center_name = serializers.SlugRelatedField(
        read_only=True, slug_field='name', source='medical_center')
    medical_center_address = serializers.SlugRelatedField(
        read_only=True, slug_field='address', source='medical_center')
    medical_center_pincode = serializers.SlugRelatedField(
        read_only=True, slug_field='pincode', source='medical_center')

    class Meta:
        model = Package
        fields = ['id', 'name', 'price', 'overview',
                  'instruction', 'medical_center', 'medical_center_name', 'medical_center_address', 'medical_center_pincode']


class PackageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageDetail
        fields = ['id', 'name']


class PackageSerializerById(serializers.ModelSerializer):
    package = PackageDetailSerializer(many=True)
    medical_center_name = serializers.CharField(
        source='medical_center', read_only=True)

    class Meta:
        model = Package
        fields = ['id', 'name', 'price', 'overview', 'instruction', 'package', 'medical_center', 'medical_center_name']


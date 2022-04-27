from rest_framework import serializers
from .models import Nurse
from accounts.serializers import UserSerializer


class NurseSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Nurse
        fields = ['id', 'address', 'primary_pincode', 'secondary_pincode', 'user_name']
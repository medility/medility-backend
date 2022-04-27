from django.shortcuts import render
from rest_framework import permissions
from knox.auth import TokenAuthentication
from rest_framework.generics import ListAPIView
from .models import Nurse
from .serializers import NurseSerializer
# Create your views here.

class NurseView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    serializer_class = NurseSerializer
    queryset = Nurse.objects.all()

    def get_object(self):
        return self.request.user



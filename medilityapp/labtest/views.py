from rest_framework import generics
from .models import LabTest
from .serializers import LabTestSerializer
# Create your views here.

class LabTestView(generics.ListAPIView):
    serializer_class = LabTestSerializer

    def get_queryset(self):
        queryset = LabTest.objects.all()
        query = self.request.query_params.get('name')
        if query is not None:
            return LabTest.objects.filter(name__icontains=query)
        return queryset


class LabTestViewById(generics.RetrieveAPIView):
    serializer_class = LabTestSerializer
    queryset = LabTest.objects.all()
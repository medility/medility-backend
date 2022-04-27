from rest_framework import generics
from .models import Package, PackageDetail
from .serializers import PackageSerializer, PackageDetailSerializer, PackageSerializerById
# Create your views here.

class PackageView(generics.ListAPIView):
    serializer_class = PackageSerializer

    def get_queryset(self):
        queryset = Package.objects.all()
        query = self.request.query_params.get('name')
        if query is not None:
            return Package.objects.filter(name__icontains=query)
        return queryset


class PackageViewById(generics.RetrieveAPIView):
    serializer_class = PackageSerializerById
    queryset = Package.objects.all()


class PackageDetailView(generics.ListAPIView):
    serializer_class = PackageDetailSerializer

    def get_queryset(self):
        queryset = PackageDetail.objects.all()
        query = self.request.query_params.get('id')
        if query is not None:
            return PackageDetail.objects.filter(packge=query)
        return queryset



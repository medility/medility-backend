from django.db import models
from medicalcenter.models import MedicalCentre

# Create your models here.
class Package(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    overview = models.CharField(max_length=200)
    instruction = models.CharField(max_length=200)
    medical_center = models.ForeignKey(MedicalCentre, related_name='package', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class PackageDetail(models.Model):
    name = models.CharField(max_length=200)
    packge = models.ForeignKey(Package, related_name='package', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
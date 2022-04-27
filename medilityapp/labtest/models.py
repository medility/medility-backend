from django.db import models
from medicalcenter.models import MedicalCentre
# Create your models here.


class LabTest(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    overview = models.CharField(max_length=400)
    instruction = models.CharField(max_length=400)
    medical_centre = models.ForeignKey(MedicalCentre, related_name='tests', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return '%s ------------------ %s' % (self.name, self.medical_centre.name)
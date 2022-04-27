from django.db import models
from nurse.models import Nurse

# Create your models here.
class TimeSlot(models.Model):
    slot = models.TimeField()

    def __str__(self):
        return str(self.slot)
    

class SlotDate(models.Model):
    slot_date = models.DateField()
    slot = models.ManyToManyField(TimeSlot, through='NurseSlot')

    def __str__(self):
        return str(self.slot_date)
    

class NurseSlot(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date_slot = models.ForeignKey(SlotDate, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    status = models.IntegerField()


    
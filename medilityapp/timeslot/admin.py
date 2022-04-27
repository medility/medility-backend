from django.contrib import admin
from .models import TimeSlot, SlotDate, NurseSlot

# Register your models here.
admin.site.register(SlotDate)
admin.site.register(TimeSlot)
admin.site.register(NurseSlot)

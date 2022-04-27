from rest_framework import serializers
from .models import SlotDate, TimeSlot, NurseSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TimeSlot
        fields = '__all__'


class DateSlotSerializer(serializers.ModelSerializer):
    slot = TimeSlotSerializer(many=True)

    class Meta: 
        model = SlotDate
        fields = ['id', 'slot_date', 'slot']



class NurseSlotSerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerializer()
    # date_slot = DateSlotSerializer()

    class Meta:
        model = NurseSlot
        fields = ['id', 'time_slot',]



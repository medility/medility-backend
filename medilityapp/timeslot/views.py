from django.shortcuts import render
from rest_framework.response import Response
from .exceptions import DateNotAvailable
from rest_framework.generics import ListAPIView
from .serializers import TimeSlotSerializer, DateSlotSerializer, NurseSlotSerializer
from .models import TimeSlot, SlotDate, NurseSlot
# Create your views here.


class DateSlotView(ListAPIView):
    serializer_class = DateSlotSerializer

    def get_queryset(self):
        queryset = SlotDate.objects.all()
        return queryset


class NurseSlotView(ListAPIView):
    serializer_class = NurseSlotSerializer

    def getIdByDate(self, queryDate):
        try:
            return SlotDate.objects.get(slot_date=queryDate)
        except SlotDate.DoesNotExist:
            raise DateNotAvailable()

    def list(self, request):
        query_date = request.query_params.get('date')
        query_pincode = request.query_params.get('pincode')
        selected_date = self.getIdByDate(query_date)
        queryset = NurseSlot.objects.filter(status=0, nurse__primary_pincode=query_pincode, date_slot=selected_date)
        serializer = NurseSlotSerializer(queryset, many=True)
        unique_slot_id = []
        unique_slots = []
        for slot in serializer.data:
            if slot['time_slot']['id'] not in unique_slot_id:
                unique_slots.append({'id': slot['id'], 'time_id': slot['time_slot']['id'], 'slot': slot['time_slot']['slot']})
                unique_slot_id.append(slot['time_slot']['id'])
        return Response(unique_slots)
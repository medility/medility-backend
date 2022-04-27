from django.urls import path, include
from appointmentinfo import views

app_name = 'appointment'

urlpatterns = [
    path('apnt/', views.AppointmentView.as_view()),
    path('apnt/save/', views.AppointmentCreateView.as_view()),
    path('apnt/nurse/', views.AppointmentByNurseView.as_view())
]

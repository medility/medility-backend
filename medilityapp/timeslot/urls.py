from django.urls import path, include
from timeslot import views

app_name = 'slot'

urlpatterns = [
        path('date/', views.DateSlotView.as_view()),
        # path('nurse/<int:pk>/', views.LabTestViewById.as_view())
        path('time/', views.NurseSlotView.as_view())
]


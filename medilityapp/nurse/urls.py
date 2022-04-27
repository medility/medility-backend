from django.urls import path, include
from nurse import views

app_name = 'nurse'

urlpatterns = [
        path('info/', views.NurseView.as_view()),
        # path('nurse/<int:pk>/', views.LabTestViewById.as_view())
]


from django.urls import path, include
from labtest import views

app_name = 'labtest'

urlpatterns = [
        path('test/', views.LabTestView.as_view()),
        path('test/<int:pk>/', views.LabTestViewById.as_view())
]


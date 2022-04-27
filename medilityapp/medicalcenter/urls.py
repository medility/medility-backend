from django.urls import path, include
from medicalcenter import views

app_name = 'center'

urlpatterns = [
    path('center/', views.Center.as_view()),
    path('center/<int:pk>/', views.CenterById.as_view())

]

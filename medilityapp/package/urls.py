from django.urls import path, include
from package import views

app_name = 'package'

urlpatterns = [
    path('pkg/', views.PackageView.as_view()),
    path('pkg/<int:pk>/', views.PackageViewById.as_view()),
    path('pkginfo/', views.PackageDetailView.as_view()),
    # path('pkginfo/<int:pk>/', views.PackageDetailViewById.as_view())
    
]

from django.urls import path, include

urlpatterns = [
    path('', include('adminsite.usermanagement.urls')),
    path('vehicle/', include('adminsite.vehicleconfiguration.urls')),
]
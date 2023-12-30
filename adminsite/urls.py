from django.urls import path, include

urlpatterns = [
    path('', include('adminsite.usermanagement.urls')),
]
from django.urls import path
from .views import (landingpage, aboutpage, termspage)

urlpatterns = [
    path('', landingpage, name="landingpage"),
    path('about-us/', aboutpage, name="aboutpage"),
    path('terms-and-conditions/', termspage, name="termspage")
]
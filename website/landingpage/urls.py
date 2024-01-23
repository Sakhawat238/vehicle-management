from django.urls import path
from .views import (landingpage, aboutpage, termspage, register, loginv,
    logoutv)

urlpatterns = [
    path('', landingpage, name="landingpage"),
    path('about-us/', aboutpage, name="aboutpage"),
    path('terms-and-conditions/', termspage, name="termspage"),
    path('register/', register, name="customerregister"),
    path('login/', loginv, name="customerlogin"),
    path('logout/', logoutv, name="customerlogout"),
]
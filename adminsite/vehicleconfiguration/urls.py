from django.urls import path
from .views import (categorylist, categoryadd, categoryedit, categorydelete,
                    vehiclelist, vehicleadd, vehicleedit, vehicledelete) 

urlpatterns = [
    path("categories/", categorylist, name="categorylist"),
    path("categories/add/", categoryadd, name="categoryadd"),
    path("categories/edit/<int:id>/", categoryedit, name="categoryedit"),
    path("categories/delete/<int:id>/", categorydelete, name="categorydelete"),
    path("vehicles/", vehiclelist, name="vehiclelist"),
    path("vehicles/add/", vehicleadd, name="vehicleadd"),
    path("vehicles/edit/<int:id>/", vehicleedit, name="vehicleedit"),
    path("vehicles/delete/<int:id>/", vehicledelete, name="vehicledelete")
]
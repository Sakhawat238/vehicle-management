from django.urls import path
from .views import (categorylist, categoryadd, categoryedit, categorydelete) 

urlpatterns = [
    path("categories/", categorylist, name="categorylist"),
    path("categories/add/", categoryadd, name="categoryadd"),
    path("categories/edit/<int:id>/", categoryedit, name="categoryedit"),
    path("categories/delete/<int:id>/", categorydelete, name="categorydelete")
]
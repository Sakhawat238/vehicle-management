from django.urls import path
from django.views.generic.base import RedirectView
from .views import (login_page, logout_view, dashboard, userlist, useradd,
                    useredit, userdelete, customerlist)

urlpatterns = [
    path('', RedirectView.as_view(url='login/')),
    path('login/', login_page, name="loginpage"),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name="dashboard"),
    path('users/', userlist, name="adminuserlist"),
    path('users/add', useradd, name="adminuseradd"),
    path('users/edit/<int:id>/', useredit, name="adminuseredit"),
    path('users/delete/<int:id>/', userdelete, name="adminuserdelete"),
    path('customers/', customerlist, name="customerlist"),
]
from django.db import models
from adminsite.usermanagement.models import User


class Category(models.Model):
    name = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.name


class Driver(models.Model):
    name= models.CharField(max_length=100, default="")
    contact_info = models.TextField(default="")
    license_info = models.TextField(default="")

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=150, default="")
    description = models.TextField(default="")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    capacity = models.PositiveIntegerField(default=2)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='thumbnail/')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name
    

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='image/')

    def __str__(self):
        return self.vehicle.name
    

class VehicleRent(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.username + " -> " + self.vehicle.name
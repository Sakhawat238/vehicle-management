import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class USER_TYPE(models.TextChoices):
    ADMIN = 'admin'
    VISITOR = 'visitor'
    DRIVER = 'driver'


class User(AbstractUser):
    slug = models.CharField(max_length=255, default=uuid.uuid4, null=True, blank=True)
    type = models.CharField(max_length=255, choices=USER_TYPE.choices)
    mobile = models.CharField(max_length=32, blank=True, null=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username + ' -> ' + self.type
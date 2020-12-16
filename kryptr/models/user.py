from django.db import models
from django.utils import timezone

class KryptrUser():

    class RoleType(models.TextChoices):
        admin = 'Admin'
        distributor = 'Distributor'
        reseller = 'Reseller'
        subreseller = 'Sub Reseller'
        support = 'Support'

    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(choices=RoleType.choices, default=RoleType.support)
    date_created = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
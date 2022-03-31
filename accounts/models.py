from django.contrib.auth.models import User
from django.db import models


class house(models.Model):
    housing_lot = models.CharField(max_length=255)


class homeOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    house = models.ForeignKey(house, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    family_code = models.CharField(max_length=255, default="NULL")

    def __str__(self):
        return str(self.family_code) + ":" + self.house.housing_lot

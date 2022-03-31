from django.contrib.auth.models import User
from django.db import models

from accounts.models import homeOwner


class log(models.Model):
    type = models.CharField(max_length=255, default="none")
    user = models.ForeignKey(homeOwner, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    visitor_name = models.CharField(max_length=255, default="NULL")
    staff = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, blank=True, default=None)
    destination = models.CharField(max_length=255, default="NULL")
    time_stamp = models.DateTimeField(null=True,blank=True,default=None)
    is_logged = models.BooleanField(default=False)

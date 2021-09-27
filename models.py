from django.db import models


class DoorAccess(models.Model):
    door_ID = models.CharField(max_length=30)
    access_token = models.CharField(max_length=36)

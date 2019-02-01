import uuid

from django.db import models
from django.contrib.auth.models import User

class Crypto(models.Model):
    name = models.CharField(max_length=8)
    full_name = models.CharField(max_length=64)

class CryptoUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    crypto = models.ForeignKey(Crypto, on_delete=models.SET_NULL, null=True)
    favorite = models.BooleanField(default=False)
    amount = models.FloatField(default=0)
    bought_value = models.FloatField(null=True)
    sell_value = models.FloatField(null=True)

class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    key = models.UUIDField(default=uuid.uuid4)
    expired = models.BooleanField(default=False)
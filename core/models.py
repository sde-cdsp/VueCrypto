import json
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core import serializers
from django.forms import model_to_dict

def default_crypto_dict():
    return {'website': '', 'twitter': '', 'reddit': '', 'source_code': ''}

class Crypto(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=8, default="")
    urls = JSONField(default=default_crypto_dict)
    logo = models.URLField(default='')

    def as_json(self):
        return model_to_dict(self)

    @classmethod
    def default_url_keys(cls):
        return cls._meta.get_field('urls').default().keys()


class CryptoUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    crypto = models.ForeignKey(Crypto, on_delete=models.SET_NULL, null=True)
    favorite = models.BooleanField(default=False)
    amount = models.FloatField(default=0)
    bought_value = models.FloatField(null=True)
    sell_value = models.FloatField(null=True)

    def as_json(self):
        data = model_to_dict(self)
        data.update(self.crypto.as_json())
        return data

    class Meta:
        unique_together = (('user', 'crypto'))


class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    key = models.UUIDField(default=uuid.uuid4)
    expired = models.BooleanField(default=False)
from django.http import JsonResponse
from django.shortcuts import render
from core.models import Crypto
from django.contrib.auth.models import User
import json
from django.core import serializers


def signup(request):
    return

def login(request):
    return

def add_crypto(request, user_id, crypto_name):
    return

def user_cryptos(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        data = {"user": None}
        return JsonResponse(json.dumps(data))
    cryptos_qs = user.cryptos_set.all()
    data = serializers.serialize('json', cryptos_qs, fields={'user__username', 'name', 'full_name'})
    return JsonResponse(data)
import json

from braces.views import JSONResponseMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.generic import View, TemplateView


@method_decorator(ensure_csrf_cookie, name="get")
class IndexView(TemplateView):
    template_name = "application.html"


class LoginUser(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except:
            return self.render_json_response({'error': "Wrong username"}, status=500)
        if request.user != user:  # user is not authenticated
            user = authenticate(username=user.username, password=request.POST.get('password'))
            if user is not None:
                login(request, user)
            else:
                return self.render_json_response({'error': "Wrong password"}, status=500)
        return self.render_json_response({}, status=200)


class LogoutUser(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return self.render_json_response({}, status=200)

def signup(request):
    return
#
# def login(request):
#     return JsonResponse({"toto": "toto"})

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
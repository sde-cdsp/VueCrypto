import json

from braces.views import JSONResponseMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, TemplateView
from django.core import serializers

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie


@method_decorator(ensure_csrf_cookie, name="get")
class IndexView(TemplateView):
    template_name = "application.html"


class LoginUser(JSONResponseMixin, View):

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except:
            return self.render_json_response({'error': "User does not exist"}, status=500)
        if request.user != user:  # user is not authenticated
            user = authenticate(username=user.username, password=request.POST.get('password'))
            if user is not None:
                login(request, user)
            else:
                return self.render_json_response({'error': "Bad password"}, status=500)
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
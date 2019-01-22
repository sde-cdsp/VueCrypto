import json

from braces.views import JSONResponseMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.views.generic import View, TemplateView
from django.core import serializers

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

class IndexView(TemplateView):
    template_name = "application.html"


@method_decorator(csrf_protect, name='post')
class LoginUser(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        token = get_token(request)
        return self.render_json_response({'csrf_token': token, 'request': json.dumps(request.__dict__)}, status=200)  # FIXME: how to send request to Vue then send it back to check csrf?

    def post(self, request, *args, **kwargs):
        # reason = CsrfViewMiddleware().process_view(request, None, (), {})
        # if reason is not None:
        #     return self.render_json_response({'error': "failed csrf"}, status=400)
        try:
            user = User.objects.get(username=request.POST.get('username'), password=request.POST.get('password'))
        except:
            return self.render_json_response({'error': "bad username or password"})
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
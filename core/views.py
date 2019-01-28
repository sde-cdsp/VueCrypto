import json

from braces.views import JSONResponseMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View, TemplateView


@method_decorator(ensure_csrf_cookie, name="get")
class IndexView(TemplateView):
    template_name = "application.html"


class RegisterUser(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        if User.objects.filter(username=request.POST.get('username')).exists():
            return self.render_json_response({'error': {"username": ["Username not available"]}}, status=500)
        elif User.objects.filter(email=request.POST.get('email')).exists():
            return self.render_json_response({'error': {"email": ["A User is already registered with this email address"]}}, status=500)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=request.POST.get('email'),
            )
            return self.render_json_response({}, status=200)
        return self.render_json_response({'error': form.errors}, status=500)


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


# class LoginUser2(LoginView):
#     def render_to_response(self, context, **response_kwargs):
#         return JsonResponse(context)

    # def form_valid(self, form):
    #     """Security check complete. Log the user in."""
    #     login(self.request, form.get_user())
    #     return JsonResponse({'form': form}, status=200)
    #
    # def form_invalid(self, form):
    #     print(form)
    #     return JsonResponse({'errors': form.errors}, status=500)


class LogoutUser(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return self.render_json_response({}, status=200)


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
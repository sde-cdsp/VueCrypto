import json

from braces.views import JSONResponseMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View, TemplateView

from core.models import ResetPassword


@method_decorator(ensure_csrf_cookie, name="get")
class IndexView(TemplateView):
    template_name = "application.html"


class RegisterUser(JSONResponseMixin, View):
    def post(self, request):
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
    def post(self, request):
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except:
            return self.render_json_response({'error': {"username": ["Wrong username."]}}, status=500)
        if request.user != user:  # user is not authenticated
            user = authenticate(username=user.username, password=request.POST.get('password'))
            if user is not None:
                login(request, user)
            else:
                return self.render_json_response({'error': {"password": ["Wrong password."]}}, status=500)
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
    def post(self, request):
        logout(request)
        return self.render_json_response({})


class AskResetPasswordView(JSONResponseMixin, View):
    def reset_password(self, request, user):
        rp = ResetPassword.objects.create(user=user)
        full_url = ''.join(['http://', get_current_site(request).domain, '/reset_password?key=%s' % rp.key])
        # User.email_user("Reset Password Request", """Link to reset your password: %s""" % full_url, from_email=None)
        print(full_url)

    def post(self, request):
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except:
            return self.render_json_response({'error': {"username": ["No e-mail associated with this username"]}}, status=500)
        self.reset_password(request, user)
        return self.render_json_response({})


class ResetPasswordView(JSONResponseMixin, View):
    def get(self, request):
        try:
            rp = ResetPassword.objects.get(key=request.POST.get('key'))
        except:
            return self.render_json_response({'error': {"key": ["The link is invalid."]}},
                                             status=500)
        return self.render_json_response({'username': rp.user.username})

    def post(self, request):
        pw = request.POST.get('password')
        try:
            validate_password(pw)
        except ValidationError as e:
            return self.render_json_response({'error': {"password": e.messages}}, status=500)
        user = User.objects.get(username=request.POST.get('username'))
        user.set_password(request.POST.get('password'))
        user.save()
        return self.render_json_response({})

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
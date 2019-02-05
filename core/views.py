import requests
from braces.views import JSONResponseMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.generic import TemplateView

from core.models import ResetPassword, CryptoUser, Crypto
from VueCrypto.settings import EMAIL_HOST_USER
import VueCrypto.configs as configs

ENDPOINT = 'v1/cryptocurrency/info'


@method_decorator(ensure_csrf_cookie, name="get")
class IndexView(JSONResponseMixin, TemplateView):
    template_name = "application.html"

    def render_to_json(self, context_data={}, status=200):
        context_data['username'] = self.request.user.username if not self.request.user.is_anonymous else ""
        print(context_data)
        return self.render_json_response(context_data, status)


class GetUser(IndexView):
    def get(self, request, *args, **kwargs):
        return self.render_to_json()


class RegisterUser(IndexView):
    def post(self, request):
        if User.objects.filter(username=request.POST.get('username')).exists():
            return self.render_to_json({'error': {"username": ["Username not available"]}}, status=500)
        elif User.objects.filter(email=request.POST.get('email')).exists():
            return self.render_to_json({'error': {"email": ["A User is already registered with this email address"]}}, status=500)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=request.POST.get('email'),
            )
            return self.render_to_json({}, status=200)
        return self.render_to_json({'error': form.errors}, status=500)


class LoginUser(IndexView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except ObjectDoesNotExist:
            return self.render_to_json({'error': {"username": ["Wrong username."]}}, status=500)
        if request.user.is_anonymous:  # user is not authenticated
            user = authenticate(username=user.username, password=request.POST.get('password'))
            if user is not None:
                login(request, user)
            else:
                return self.render_to_json({'error': {"password": ["Wrong password."]}}, status=500)
        return self.render_to_json({}, status=200)


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


class LogoutUser(IndexView):
    def post(self, request):
        logout(request)
        return self.render_to_json({})


class AskPasswordResetView(IndexView):
    template_name = "application.html"

    def reset_password(self, request, user):
        rp = ResetPassword.objects.create(user=user)
        full_url = ''.join(['http://', get_current_site(request).domain, '/password_reset?username=%s&key=%s' % (user.username, rp.key)])
        send_mail(subject="Reset Password Request", message="""Link to reset your password: %s""" % full_url, from_email=EMAIL_HOST_USER, recipient_list=[user.email])

    def post(self, request):
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except ObjectDoesNotExist:
            return self.render_to_json({'error': {"username": ["No e-mail associated with this username"]}}, status=500)
        self.reset_password(request, user)
        return self.render_to_json({})


class PasswordResetView(IndexView):
    def get(self, request, *args, **kwargs):
        try:
            rp = ResetPassword.objects.get(key=request.GET.get('key'), user__username=request.GET.get('username'), expired=False)
            if rp.expired:
                return self.render_to_json({'error': {"key": ["The link is invalid."]}}, status=500)
        except ObjectDoesNotExist:
            return self.render_to_json({'error': {"key": ["The link is invalid."]}}, status=500)
        return render(request, 'application.html', {'username': rp.user.username, 'key': rp.key})

    def post(self, request):
        try:
            username = request.POST.get('username')
            rp = ResetPassword.objects.get(key=request.POST.get('key'), user__username=username)
            if rp.expired:
                return self.render_to_json({'error': {"resetpw": ["Link expired."]}})
        except (ObjectDoesNotExist, ValidationError):
            return self.render_to_json({'error': {"resetpw": ["Invalid. Please retry from the link you received by e-mail."]}})

        form = SetPasswordForm(User.objects.get(username=username), request.POST)
        if form.is_valid():
            form.save()
            return self.render_to_json({})
        return self.render_to_json({'error': form.errors}, status=500)


def add_crypto(request, user_id, crypto_name):
    return


class AddCrypto(IndexView):
    CMC_ENDPOINT = 'v1/cryptocurrency/info'

    def post(self, request):
        def data_crypto(data):
            urls = {k: data['urls'][k][0] for k in Crypto.default_url_keys() if data['urls'][k]}
            return {
                'urls': urls,
                'logo': data['logo'],
                'symbol': data['symbol'],
                'name': data['name']
            }

        def get_or_create_crypto(data):
            try:
                return Crypto.objects.get(symbol=data['symbol'])
            except ObjectDoesNotExist:
                return Crypto.objects.create(**data)

        def add_user(c):
            try:
                CryptoUser.objects.create(crypto=c, user=request.user)
            except IntegrityError:
                pass

        if request.user.is_anonymous():
            return self.render_to_json()

        symbol = request.POST.get('symbol')
        r = requests.get(configs.CMC_DOMAIN + self.CMC_ENDPOINT, params=({'symbol': symbol}), headers={'X-CMC_PRO_API_KEY': configs.CMC_KEY})
        response = r.json()

        crypto = data_crypto(response['data'][symbol])
        c = get_or_create_crypto(crypto)
        add_user(c)

        return self.render_to_json(response)


class RemoveCrypto(IndexView):
    def get(self, request, *args, **kwargs):
        return self.render_to_json()


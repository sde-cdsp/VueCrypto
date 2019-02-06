"""VueCrypto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="app"),
    path('get_user_connected/', GetUser.as_view()),
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('ask_password_reset/', AskPasswordResetView.as_view()),
    path('password_reset/', PasswordResetView.as_view()),
    path('logout/', LogoutUser.as_view()),
    path('<int:id>/<str:name>', add_crypto),
    path('user_crypto', UserCrypto.as_view()),
    path('remove_cryptos', RemoveCrypto.as_view()),
]

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from task_manager.mixins import CustomMessageMixin


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(CustomMessageMixin, LoginView):
    flash_message = _('Logged_in')
    message_type = 'success'

    template_name = 'users/login.html'
    form_class = AuthenticationForm


class UserLogoutView(CustomMessageMixin, LogoutView):
    flash_message = _('Logged_out')
    message_type = 'info'

    template_name = 'users/login.html'
    form_class = AuthenticationForm


class Error404View(TemplateView):
    template_name = 'errors/404.html'


class Error500View(TemplateView):
    template_name = 'errors/500.html'

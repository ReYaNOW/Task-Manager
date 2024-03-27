from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.utils import CustomMessageMixin


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class UserLoginView(CustomMessageMixin, LoginView):
    flash_message = _('Logged_in')
    message_type = 'success'

    template_name = 'login.html'
    form_class = AuthenticationForm


class UserLogoutView(CustomMessageMixin, LogoutView):
    flash_message = _('Logged_out')
    message_type = 'info'

    template_name = 'login.html'
    form_class = AuthenticationForm

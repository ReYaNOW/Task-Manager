from django.contrib import messages
from django.db.models import ProtectedError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('Arent authorized'))
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


class CustomPermissionRequiredMixin(UserPassesTestMixin):
    permission_url = None
    permission_message = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class CheckAuthorMixin(CustomPermissionRequiredMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class CustomMessageMixin:
    """
    Add a custom type message on successful page.
    """

    flash_message = ''
    message_type = ''

    def get_success_url(self):
        success_url = super().get_success_url()
        getattr(messages, self.message_type)(self.request, self.flash_message)
        return success_url

    def get_flash_message(self, cleaned_data):
        return self.flash_message % cleaned_data


class ProtectedErrorHandlerMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)

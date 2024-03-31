from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('Arent authorized'))
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


class CustomPermissionRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('id') != request.user.id:
            messages.error(request, _('Dont have permissions to change'))
            return redirect('users_index')

        return super().dispatch(request, *args, **kwargs)


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

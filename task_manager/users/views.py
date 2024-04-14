from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from task_manager.utils import (
    CustomLoginRequiredMixin,
    CustomPermissionRequiredMixin,
)
from .forms import UserCreateForm, UserUpdateForm


class IndexView(ListView):
    template_name = 'index_pages/users_index.html'

    model = User
    context_object_name = 'users'


class UserFormCreateView(SuccessMessageMixin, CreateView):
    template_name = 'crud_parts/create.html'
    extra_context = {'title': _('Sign Up')}

    model = User
    form_class = UserCreateForm

    success_url = reverse_lazy('login')
    success_message = _('Sign up success')


class UserFormUpdateView(
    CustomLoginRequiredMixin,
    CustomPermissionRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = 'crud_parts/update.html'
    extra_context = {'title': _('Change user')}

    model = User
    form_class = UserUpdateForm

    success_url = reverse_lazy('users_index')
    success_message = _('Edit success')


class UserFormDeleteView(
    CustomLoginRequiredMixin,
    CustomPermissionRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = 'crud_parts/delete.html'
    extra_context = {'title': _('Deleting user')}

    model = User

    success_url = reverse_lazy('users_index')
    success_message = _('Delete success')

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from task_manager.mixins import (
    CustomLoginRequiredMixin,
    ProtectedErrorHandlerMixin,
)
from .forms import StatusCreateForm
from .models import Status


class StatusListView(CustomLoginRequiredMixin, ListView):
    template_name = 'statuses/statuses_list.html'

    model = Status
    context_object_name = 'statuses'


class StatusCreateView(SuccessMessageMixin, CreateView):
    template_name = 'crud_parts/create.html'
    extra_context = {'title': _('Create status'), 'button_text': _('Create')}

    model = Status
    form_class = StatusCreateForm

    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully created')


class StatusUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = 'crud_parts/update.html'
    extra_context = {'title': _('Change status')}

    model = Status
    form_class = StatusCreateForm

    success_url = reverse_lazy('statuses_list')
    success_message = _('Status changed successfully')


class StatusDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    ProtectedErrorHandlerMixin,
    DeleteView,
):
    template_name = 'crud_parts/delete.html'
    extra_context = {'title': _('Deleting status')}

    model = Status

    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully deleted')

    protected_url = reverse_lazy('statuses_list')
    protected_message = _('status_in_usage')

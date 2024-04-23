from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from task_manager.mixins import (
    CustomLoginRequiredMixin,
    ProtectedErrorHandlerMixin,
)
from .forms import LabelCreateForm
from .models import Label


class LabelListView(CustomLoginRequiredMixin, ListView):
    template_name = 'labels/labels_list.html'

    model = Label
    context_object_name = 'labels'


class LabelCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    template_name = 'crud_parts/create.html'
    extra_context = {'title': _('Create label')}

    model = Label
    form_class = LabelCreateForm

    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')


class LabelUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = 'crud_parts/update.html'
    extra_context = {'title': _('Change label')}

    model = Label
    form_class = LabelCreateForm

    success_url = reverse_lazy('labels_list')
    success_message = _('Label changed successfully')


class LabelDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    ProtectedErrorHandlerMixin,
    DeleteView,
):
    template_name = 'crud_parts/delete.html'
    extra_context = {'title': _('Deleting label')}

    model = Label

    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully deleted')

    protected_url = reverse_lazy('labels_list')
    protected_message = _('label_in_usage')

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from task_manager.utils import CustomLoginRequiredMixin
from .forms import StatusCreateForm
from .models import Status


class IndexView(ListView):
    template_name = 'index_pages/statuses_index.html'

    model = Status
    context_object_name = 'statuses'


class StatusFormCreateView(SuccessMessageMixin, CreateView):
    template_name = 'crud_parts/create.html'
    extra_context = {'title': _('Create status')}

    model = Status
    form_class = StatusCreateForm

    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully created')


class StatusFormUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = 'crud_parts/update.html'
    extra_context = {'title': _('Change status')}

    model = Status
    form_class = StatusCreateForm

    success_url = reverse_lazy('statuses_index')
    success_message = _('Status changed successfully')


class StatusFormDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = 'crud_parts/delete.html'
    extra_context = {'title': _('Deleting status')}

    model = Status

    success_url = reverse_lazy('statuses_index')
    success_message = _('Status successfully deleted')

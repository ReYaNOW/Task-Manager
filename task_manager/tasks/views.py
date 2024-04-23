from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django_filters.views import FilterView

from task_manager.mixins import (
    CustomLoginRequiredMixin,
    CheckAuthorMixin,
)
from .filter import TaskFilter
from .forms import TaskCreateForm
from .models import Task


class TaskListView(CustomLoginRequiredMixin, FilterView):
    template_name = 'tasks/tasks_list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    template_name = 'tasks/task_read.html'
    extra_context = {'title': _('Task view')}
    model = Task


class TaskCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    template_name = 'crud_parts/create.html'
    extra_context = {'title': _('Create task')}

    model = Task
    form_class = TaskCreateForm

    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class TaskUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = 'crud_parts/update.html'
    extra_context = {'title': _('Change task')}

    model = Task
    form_class = TaskCreateForm

    success_url = reverse_lazy('tasks_list')
    success_message = _('Task changed successfully')


class TaskDeleteView(
    CustomLoginRequiredMixin,
    CheckAuthorMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = 'crud_parts/delete.html'
    extra_context = {'title': _('Deleting task')}

    model = Task

    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully deleted')

    permission_url = reverse_lazy('tasks_list')
    permission_message = _('task_no_permissions')

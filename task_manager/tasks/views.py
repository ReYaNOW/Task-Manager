from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from task_manager.utils import (
    CustomLoginRequiredMixin,
    CheckAuthorMixin,
)
from .forms import TaskCreateForm, SearchForm
from .models import Task


class IndexView(CustomLoginRequiredMixin, View):
    def get(self, request):
        form = SearchForm()
        tasks = Task.objects.all()

        return render(
            request,
            'index_pages/tasks_index.html',
            context={'tasks': tasks, 'form': form},
        )

    def post(self, request):
        form = SearchForm(request.POST)
        tasks = Task.objects.all()

        if form.is_valid():
            for param, value in form.cleaned_data.items():
                if value:
                    if param == 'only_own_tasks':
                        tasks = tasks.filter(author=request.user)
                    else:
                        tasks = tasks.filter(**{param: value})

        return render(
            request,
            'index_pages/tasks_index.html',
            {'tasks': tasks, 'form': form},
        )


class TaskView(CustomLoginRequiredMixin, DetailView):
    template_name = 'crud_parts/task_read.html'
    extra_context = {'title': _('Task view')}
    model = Task


class TaskFormCreateView(
    SuccessMessageMixin, CustomLoginRequiredMixin, CreateView
):
    template_name = 'crud_parts/create.html'
    extra_context = {'title': _('Create task')}

    model = Task
    form_class = TaskCreateForm

    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class TaskFormUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    template_name = 'crud_parts/update.html'
    extra_context = {'title': _('Change task')}

    model = Task
    form_class = TaskCreateForm

    success_url = reverse_lazy('tasks_index')
    success_message = _('Task changed successfully')


class TaskFormDeleteView(
    CustomLoginRequiredMixin,
    CheckAuthorMixin,
    SuccessMessageMixin,
    DeleteView,
):
    template_name = 'crud_parts/delete.html'
    extra_context = {'title': _('Deleting task')}

    model = Task

    success_url = reverse_lazy('tasks_index')
    success_message = _('Task successfully deleted')

    permission_url = reverse_lazy('tasks_index')
    permission_message = _('task_no_permissions')

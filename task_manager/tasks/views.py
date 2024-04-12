from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.utils import CustomLoginRequiredMixin
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


class TaskView(CustomLoginRequiredMixin, View):
    def get(self, request, id):
        task = get_object_or_404(Task, id=id)

        return render(
            request,
            'crud_parts/task_read.html',
            context={'task': task},
        )


class TaskFormCreateView(CustomLoginRequiredMixin, View):
    def get(self, request):
        print(1)
        form = TaskCreateForm()
        return render(request, 'crud_parts/create.html', {'form': form})

    def post(self, request):
        form = TaskCreateForm(request.POST)
        form.instance.author = User.objects.get(id=self.request.user.id)
        if form.is_valid():
            form.save()
            messages.success(request, _('Task successfully created'))
            return redirect('tasks_index')
        return render(request, 'crud_parts/create.html', {'form': form})


class TaskFormUpdateView(CustomLoginRequiredMixin, View):
    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        form = TaskCreateForm(instance=task)
        return render(
            request, 'crud_parts/update.html', {'task': task, 'form': form}
        )

    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _('Task changed successfully'))
            return redirect('tasks_index')
        return render(request, 'crud_parts/update.html', {'form': form})


class TaskFormDeleteView(CustomLoginRequiredMixin, View):
    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        return render(request, 'crud_parts/delete.html', {'task': task})

    def post(self, request, id):
        task = get_object_or_404(Task, id=id)
        if task:
            task.delete()
            messages.success(request, _('Task successfully deleted'))
        return redirect('tasks_index')

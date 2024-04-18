from django import forms
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from .models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

        error_messages = {
            'name': {'unique': _('task_exists_message')},
        }

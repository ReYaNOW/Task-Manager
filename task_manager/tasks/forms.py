from django import forms
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

from .models import Task


class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return smart_str(user.get_full_name())


class TaskCreateForm(forms.ModelForm):
    executor = UserFullnameChoiceField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

        error_messages = {
            'name': {'unique': _('task_exists_message')},
        }

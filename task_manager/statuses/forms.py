from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Status


class StatusCreateForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']

        labels = {
            'name': _('status_name'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': True}),
        }

        error_messages = {
            'username': {'unique': _('status_exists_message')},
        }

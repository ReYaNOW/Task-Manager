from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Status


class StatusCreateForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

        labels = {
            'name': _('status_name'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

        error_messages = {
            'name': {'unique': _('status_exists_message')},
        }

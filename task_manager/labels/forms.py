from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Label


class LabelCreateForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

        labels = {
            'name': _('Name'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'autofocus': True}),
        }

        error_messages = {
            'name': {'unique': _('label_exists_message')},
        }

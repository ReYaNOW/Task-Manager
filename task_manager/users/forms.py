from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

username_validator = RegexValidator(
    r'^[a-zA-Z0-9@/./+/-/_]*', _('user_name_validation_error')
)


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": 'new-password'}),
        help_text=_('passwd_help_message'),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

        labels = {
            'first_name': _('Name'),
            'last_name': _('Surname'),
            'username': _('Nickname'),
            'password1': _('Password'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': True}),
        }

        help_texts = {'username': _('username_help_message')}

        error_messages = {
            'username': {
                'unique': _('A user with the same name already exists.'),
            },
        }

        validators = {'username': username_validator}


class UserUpdateForm(UserCreateForm):
    def clean_username(self):
        return self.cleaned_data.get('username')

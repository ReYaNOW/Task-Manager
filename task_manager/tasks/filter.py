from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(FilterSet):
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_('Label'))
    personal = BooleanFilter(
        widget=forms.CheckboxInput,
        method='get_personal_tasks',
        label=_('only_personal_tasks'),
    )

    def get_personal_tasks(self, queryset, _, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']

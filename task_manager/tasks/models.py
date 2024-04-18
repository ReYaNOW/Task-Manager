from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from task_manager.users.models import UserFullName
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(
        max_length=100, unique=True, blank=False, verbose_name=_('name')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    author = models.ForeignKey(
        UserFullName,
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='author',
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_('Status')
    )
    executor = models.ForeignKey(
        UserFullName,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        related_name='executor',
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        through='TaskLabelThrough',
        through_fields=('task', 'label'),
        verbose_name=_('Labels'),
    )

    created_at = models.DateTimeField(auto_now_add=True)


class TaskLabelThrough(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)

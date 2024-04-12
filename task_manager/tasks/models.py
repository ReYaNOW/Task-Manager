from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=100, unique=True, blank=False, verbose_name=_('name')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='author',
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_('Status')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        related_name='executor',
    )

    created_at = models.DateTimeField(auto_now_add=True)

from django.urls import path

from task_manager.statuses.views import (
    IndexView,
    StatusFormCreateView,
    StatusFormUpdateView,
    StatusFormDeleteView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='statuses_index'),
    path('create/', StatusFormCreateView.as_view(), name='status_create'),
    path(
        '<int:id>/edit/', StatusFormUpdateView.as_view(), name='status_update'
    ),
    path(
        '<int:id>/delete/',
        StatusFormDeleteView.as_view(),
        name='status_delete',
    ),
]

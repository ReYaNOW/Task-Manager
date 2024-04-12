from django.urls import path

from task_manager.users.views import (
    IndexView,
    UserFormCreateView,
    UserFormUpdateView,
    UserFormDeleteView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='users_index'),
    path('create/', UserFormCreateView.as_view(), name='user_create'),
    path('<int:id>/update/', UserFormUpdateView.as_view(), name='user_update'),
    path('<int:id>/delete/', UserFormDeleteView.as_view(), name='user_delete'),
]

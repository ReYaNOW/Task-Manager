from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.translation import gettext_lazy as _

from task_manager.utils import (
    CustomLoginRequiredMixin,
    CustomPermissionRequiredMixin,
)
from .forms import UserCreateForm, UserUpdateForm


class IndexView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users/index.html', context={'users': users})


class UserFormCreateView(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Sign up success'))
            return redirect('login')

        return render(request, 'users/create.html', {'form': form})


class UserFormUpdateView(
    CustomLoginRequiredMixin, CustomPermissionRequiredMixin, View
):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = UserUpdateForm(instance=user)
        return render(request, 'users/update.html', {'form': form})

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Edit success'))
            logout(request)
            return redirect('users_index')

        return render(request, 'users/update.html', {'form': form})


class UserFormDeleteView(
    CustomLoginRequiredMixin, CustomPermissionRequiredMixin, View
):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        return render(request, 'users/delete.html', {'user': user})

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        if user:
            logout(request)
            user.delete()
            messages.success(request, _('Delete success'))
        return redirect('users_index')

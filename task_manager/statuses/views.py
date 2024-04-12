from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.utils import CustomLoginRequiredMixin
from .forms import StatusCreateForm
from .models import Status


class IndexView(CustomLoginRequiredMixin, View):
    def get(self, request):
        statuses = Status.objects.all()
        return render(
            request, 'statuses/index.html', context={'statuses': statuses}
        )


class StatusFormCreateView(CustomLoginRequiredMixin, View):
    def get(self, request):
        form = StatusCreateForm()
        return render(request, 'statuses/create.html', {'form': form})
    
    def post(self, request):
        form = StatusCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully created'))
            return redirect('statuses_index')
        
        return render(request, 'statuses/create.html', {'form': form})


class StatusFormUpdateView(CustomLoginRequiredMixin, View):
    def get(self, request, id):
        status = get_object_or_404(Status, id=id)
        form = StatusCreateForm(instance=status)
        return render(
            request, 'statuses/update.html', {'form': form, 'id': id}
        )
    
    def post(self, request, id):
        status = get_object_or_404(Status, id=id)
        form = StatusCreateForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status changed successfully'))
            return redirect('statuses_index')
        
        return render(
            request, 'statuses/update.html', {'form': form}
        )


class StatusFormDeleteView(CustomLoginRequiredMixin, View):
    def get(self, request, id):
        status = get_object_or_404(Status, id=id)
        return render(request, 'statuses/delete.html', {'status': status})
    
    def post(self, request, id):
        status = get_object_or_404(Status, id=id)
        if status:
            status.delete()
            messages.success(request, _('Status successfully deleted'))
        return redirect('statuses_index')

from django.views.generic.base import TemplateView
from django.shortcuts import render


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

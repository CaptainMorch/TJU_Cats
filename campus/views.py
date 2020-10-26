from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Location

from campus.models import Campus

import json


# Create your views here.
class LocationCreateView(CreateView):
    model = Location
    fields = '__all__'
    success_url = reverse_lazy('cat:list')
    template_name = "campus/create_location.html"

    def get_context_data(self, *args, **kwargs):
        """将所有校区信息以字典形式传入模板"""
        context = super().get_context_data(*args, **kwargs)

        campuses = Campus.objects.values()
        context['campuses'] = campuses
        context['campuses_json'] = json.dumps(list(campuses))

        return context

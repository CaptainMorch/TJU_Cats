from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Cat
from .actions import enabled_actions


# Create your views here.
class CatListView(ListView):
    queryset = Cat.objects.exclude(
        status=Cat.STATUS_CHOICES.get_val('离世')
        ).exclude(
        status=Cat.STATUS_CHOICES.get_val('失踪')
        )
    paginate_by = 20


class CatDetailView(DetailView):
    model = Cat

    def get_context_data(self, **kwargs):
        """带上预渲染好的可用操作列表"""
        context = super().get_context_data(**kwargs)
        actions = []
        for action in enabled_actions:
            if action.has_action(self.object):
                actions.append(action.render_components(self.object))
        context['actions'] = actions
        return context
        

class CatCreateView(CreateView):
   model = Cat
   fields = '__all__'


class CatUpdateView(UpdateView):
    model = Cat
    fields = '__all__'
    template_name = 'cat/cat_form.html'
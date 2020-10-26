from django.views.generic import DetailView, CreateView
from .models import Photo


# Create your views here.
class PhotoDetailView(DetailView):
    model = Photo
    template_name = "file/photo.html"


class PhotoCreateView(CreateView):
    model = Photo
    template_name = "file/photo_create.html"
    fields = '__all__'

    def get_success_url(self):
        cat = self.object.cats.all()[0]
        return cat.get_absolute_url()

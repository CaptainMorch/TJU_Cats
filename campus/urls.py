from django.urls import path

from .views import LocationCreateView

app_name = 'campus'
urlpatterns = [
    path('location/create/', LocationCreateView.as_view(), name='create_location'),
]

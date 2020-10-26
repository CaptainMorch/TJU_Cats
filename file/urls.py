from django.urls import path
from . import views


app_name = 'file'
urlpatterns = [
    path('create/', views.PhotoCreateView.as_view(), name='upload_photo'),
    path('{int:pk}/', views.PhotoDetailView.as_view(), name='photo'),
]
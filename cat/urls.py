from django.urls import path, include

from utilties import actions_urlpatterns
from .actions import enabled_actions
from .views import CatCreateView, CatDetailView, CatListView, CatUpdateView

app_name = 'cat'
action_patterns = actions_urlpatterns(*enabled_actions)
urlpatterns = [
    path('', CatListView.as_view(), name='list'),
    path('<int:pk>/', CatDetailView.as_view(), name='detail'),
    path('create/', CatCreateView.as_view(), name='create'),
    path('<int:pk>/update', CatUpdateView.as_view(), name='update'),
    path('<int:pk>/action/', include(action_patterns)),
]

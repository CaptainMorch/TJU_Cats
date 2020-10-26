"""cats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
# from django.conf.urls.static import static

# import debug_toolbar


urlpatterns = [
    path('bdmin/admin/', admin.site.urls),
    # path('__debug__/', include(debug_toolbar.urls)),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
    
    path('campus/', include('campus.urls', namespace='campus')),
    path('file/', include('file.urls', namespace='file')),
    path('cats/', include('cat.urls', namespace='cat')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
]


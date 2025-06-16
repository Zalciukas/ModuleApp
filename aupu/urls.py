"""
URL configuration for vapa project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),  # Pridėti šią eilutę
    path('modules/', include('modules.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
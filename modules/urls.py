from django.urls import path
from .views import (
    ModuleListView, ModuleCreateView, ModuleUpdateView, 
    ModuleDeleteView, generate_modules_pdf
)

app_name = 'modules'

urlpatterns = [
    path('', ModuleListView.as_view(), name='list'),
    path('add/', ModuleCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', ModuleUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ModuleDeleteView.as_view(), name='delete'),
    path('pdf/', generate_modules_pdf, name='pdf'),
]
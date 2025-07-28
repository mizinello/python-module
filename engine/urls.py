from django.urls import path
from . import views

app_name = 'engine'

urlpatterns = [
    path('', views.module_list_view, name='module-list'),
    path('install/<str:module_name>/', views.install_module, name='module-install'),
    path('uninstall/<str:module_name>/', views.uninstall_module, name='module-uninstall'),
    path('upgrade/<str:module_name>/', views.upgrade_module, name='module-upgrade'),
]

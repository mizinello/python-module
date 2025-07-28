from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('module/', include('engine.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Muat URL hanya jika module aktif
try:
    from engine.models import InstalledModule
    if InstalledModule.objects.filter(name='product_module', is_active=True).exists():
        urlpatterns += [path('product/', include('product_module.urls'))]
except:
    pass
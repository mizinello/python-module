from django.shortcuts import render, redirect
from .models import InstalledModule
import subprocess
import sys
from django.conf import settings

MODULES = {
    'product_module': {
        'verbose_name': 'Product Module',
        'url': '/product/',
    }
}

def module_list_view(request):
    installed = InstalledModule.objects.all()
    return render(request, 'engine/module_list.html', {
        'modules': MODULES,
        'installed': {mod.name: mod for mod in installed}
    })

def install_module(request, module_name):
    mod, _ = InstalledModule.objects.get_or_create(name=module_name)
    mod.is_active = True
    mod.save()
    return redirect('engine:module-list')

def uninstall_module(request, module_name):
    InstalledModule.objects.filter(name=module_name).delete()
    return redirect('engine:module-list')

def upgrade_module(request, module_name):
    mod = InstalledModule.objects.get(name=module_name)
    mod.version = "1.1.0"
    mod.save()

    try:
        subprocess.run(
            [sys.executable, 'manage.py', 'makemigrations', module_name],
            check=True,
            cwd=settings.BASE_DIR
        )
        subprocess.run(
            [sys.executable, 'manage.py', 'migrate', module_name],
            check=True,
            cwd=settings.BASE_DIR
        )
    except subprocess.CalledProcessError as e:
        print(f"Upgrade failed: {e}")

    return redirect('engine:module-list')

from django.db import models

class InstalledModule(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    version = models.CharField(max_length=20, default='1.0.0')

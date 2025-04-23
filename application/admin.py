from django.contrib import admin
from .models import Patient, Scan, Image

# Register your models here.
admin.site.register(Patient)
admin.site.register(Scan)
admin.site.register(Image)
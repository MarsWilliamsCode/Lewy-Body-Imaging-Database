from django.contrib import admin
from .models import Patient, Scan, Image, Annotation

# Register your models here.
admin.site.register(Patient)
admin.site.register(Scan)
admin.site.register(Image)
admin.site.register(Annotation)
from django.contrib import admin
from .models import Patient, Scan, Image

# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ("scan_id", )

@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    search_fields = ('scan_id',)
    autocomplete_fields = ("patient_id",)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ('patient_id',)
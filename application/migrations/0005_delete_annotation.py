# Generated by Django 5.1.7 on 2025-04-23 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_remove_scan_storage_path_image_storage_path'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Annotation',
        ),
    ]

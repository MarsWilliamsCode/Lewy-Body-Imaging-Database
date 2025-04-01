from django.shortcuts import render
from .models import Scan, Image


def scan_list(request):
    scans = Scan.objects.all()
    images = Image.objects.all()

    return render(request, 'application/scan_list.html', {'scans': scans, 'images': images})

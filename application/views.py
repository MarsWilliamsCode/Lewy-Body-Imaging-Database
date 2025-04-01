from django.shortcuts import render
from .models import Scan


def scan_list(request):
    scans = Scan.objects.all()

    return render(request, 'application/scan_list.html', {'scans': scans})

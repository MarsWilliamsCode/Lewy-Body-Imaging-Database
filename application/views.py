from django.shortcuts import render
from .models import Scan

def search_landing(request):
    return render(request, 'search_landing.html')

def scan_list(request):
    scans = Scan.objects.all()

    return render(request, "scan_list.html", {'scans': scans})



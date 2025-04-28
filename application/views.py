import io
import os
import re
import zipfile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from .models import Scan, Image
from django.db.models import Q
import logging

def search_landing(request):
    return render(request, 'search_landing.html')

def search_results(request):
    logger = logging.getLogger('django')
    def get_queryset():
        queryFilter = request.GET.get("filter")
        queryString = request.GET.get("q")
        queryList = re.split(r',\s*', queryString)

        if queryFilter == 'All':
            scan_list = Scan.objects.filter(patient_id=-1)
            for query in queryList:
                scan_list = scan_list.union(Scan.objects.filter(
                Q(scan_type__icontains=query) | Q(patient_id__diagnosis__icontains=query) | Q(patient_id__patient_id__icontains=query)
                ))

        elif queryFilter == 'Disease':
            scan_list = Scan.objects.filter(patient_id=-1)
            for query in queryList:
                scan_list = scan_list.union(Scan.objects.filter(
                Q(patient_id__diagnosis__icontains=query)
                ))

        elif queryFilter == 'Modality':
            scan_list = Scan.objects.filter(patient_id=-1)
            for query in queryList:
                scan_list = scan_list.union(Scan.objects.filter(
                    Q(scan_type__icontains=query)
                ))
        elif queryFilter == 'Stage':
            scan_list = Scan.objects.filter(patient_id=-1)
            for query in queryList:
                scan_list = scan_list.union(Scan.objects.filter(
                    Q(patient_id__disease_stage__icontains=query)
                ))
        return scan_list
    return render(request, "search_results.html", {'scans': get_queryset(), 'request': request})

def scan_page(request, scan_id):
    logger = logging.getLogger('django')
    scan = Scan.objects.get(scan_id=scan_id)
    images = Image.objects.filter(scan_id_id=scan_id)
    return render(request, "scan.html", {'scan': scan, 'images': images})

def download_zipfile(request, scan_id):
    logger = logging.getLogger('django')
    images = Image.objects.filter(scan_id_id=scan_id)
    imageList = [image.image_url for image in images]
    logger.info(imageList)
    byte_data = io.BytesIO()
    zip_name = scan_id + ".zip"

    with zipfile.ZipFile(byte_data, 'w') as zip:
        for image in imageList:
            try:
                file_name = image.split('/')[-1]
                zip.writestr(file_name, image)
            except Exception as e:
                print(e)

    byte_data.seek(0)

    response = HttpResponse(byte_data, content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename="{zip_name}"'
    return response

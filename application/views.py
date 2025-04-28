import io
import os
import re
import zipfile

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from .models import Scan, Image
from django.db.models import Q, Count
import logging

def search_landing(request):
    return render(request, 'search_landing.html')

def search_results(request):
    def get_queryset():
        queryFilter = request.GET.get("filter")
        queryString = request.GET.get("q")
        queryList = re.split(r',\s*', queryString)
        scans_with_images = Scan.objects.annotate(num_images=Count('image'))
        scans_with_images = scans_with_images.filter(num_images__gt=0)

        if queryFilter == 'All':
            scan_list = scans_with_images.filter(patient_id=-1)
            for query in queryList:
                scan_list = scan_list.union(scans_with_images.filter(
                    (Q(scan_type__icontains=query) | Q(patient_id__diagnosis__icontains=query) | Q(patient_id__patient_id__icontains=query))
                ))

        elif queryFilter == 'Disease':
            scan_list = scans_with_images.filter(patient_id=-1)
            for query in queryList:
                scan_list = scan_list.union(scans_with_images.filter(
                Q(patient_id__diagnosis__icontains=query)
                ))

        elif queryFilter == 'Modality':
            scan_list = scans_with_images.filter(patient_id=-1)
            for query in queryList:
                scan_list = scan_list.union(scans_with_images.filter(
                    Q(scan_type__icontains=query)
                ))
        elif queryFilter == 'Stage':
            scan_list = scans_with_images.filter(patient_id=-1)
            for query in queryList:
                scan_list = scan_list.union(scans_with_images.filter(
                    Q(patient_id__disease_stage__icontains=query)
                ))
        return scan_list
    scan_list = get_queryset()

    p = Paginator(scan_list, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return render(request, "search_results.html", {'page_obj': page_obj, 'request': request})

def scan_page(request, scan_id):
    scan = Scan.objects.get(scan_id=scan_id)
    images = Image.objects.filter(scan_id_id=scan_id)
    return render(request, "scan.html", {'scan': scan, 'images': images})

def download_zipfile(request, scan_id):
    images = Image.objects.filter(scan_id_id=scan_id)
    imageList = [image.image_url for image in images]
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

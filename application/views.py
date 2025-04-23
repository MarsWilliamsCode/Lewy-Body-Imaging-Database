import re

from django.shortcuts import render
from .models import Scan
from django.db.models import Q
import logging


def search_landing(request):
    return render(request, 'search_landing.html')

def search_results(request):
    logger = logging.getLogger('django')
    def get_queryset():
        queryFilter = request.GET.get("filter")
        logger.info(f"queryFilter: {queryFilter}")
        queryString = request.GET.get("q")
        queryList = re.split(r',\s*', queryString)

        logger.info(f"queryList: {queryList}")
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
        logger.info(f"scan_list: {scan_list}")
        return scan_list
    return render(request, "search_results.html", {'scans': get_queryset()})



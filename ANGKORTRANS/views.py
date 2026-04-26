# views.py
import sys
import django
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
import os
from django.http import JsonResponse
import math
from django.views.generic import TemplateView
from django.conf import settings

class HomeView(TemplateView):
    template_name = 'index.html'   # or 'home.html' depending on your choice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass values to template safely
        context['api_version'] = getattr(settings, 'API_VERSION')
        context['app_title']   = getattr(settings, 'APP_TITLE')
        context['django_version'] = django.get_version()
        context['python_version'] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        # Optional: You can remove this print in production
        # print("API Version from settings:", context['api_version'])

        return context


print(" settings.BASE_DIR =-======> ", settings.BASE_DIR)
file_path = os.path.join(settings.BASE_DIR, 'CambodiaGeographicalList2025.json')
# print(" Full path -----------> ",file_path)
# def load_data():
#     file_path = os.path.join(settings.BASE_DIR, 'CambodiaGeographicalList2025.json')
#     print(" Full path -----------> ",file_path)
#     with open(file_path, encoding='utf-8') as f:
#         return json.load(f)["items"]

from functools import lru_cache

@lru_cache(maxsize=1)
def load_data():
    file_path = os.path.join(settings.BASE_DIR, 'CambodiaGeographicalList2025.json')
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)["items"]


@lru_cache(maxsize=1)
def load_data():
    file_path = os.path.join(settings.BASE_DIR, 'CambodiaGeographicalList2025.json')
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)["items"]


def filter_address(request):
    data = load_data()

    # ======================
    # GET QUERY PARAMS
    # ======================
    province_code = request.GET.get('province_code')
    district_code = request.GET.get('district_code')
    commune_code = request.GET.get('commune_code')
    village_code = request.GET.get('village_code')

    # page = int(request.GET.get('page', 1))
    page = max(1, int(request.GET.get('page', 1)))
    page_size = min(500, max(1, int(request.GET.get('page_size', 200))))
    # page_size = int(request.GET.get('page_size', 200))

    # ======================
    # FILTERING (OPTIONAL)
    # ======================
    results = data

    if province_code:
        results = [i for i in results if i["province_code"] == int(province_code)]

    if district_code:
        results = [i for i in results if i["district_code"] == int(district_code)]

    if commune_code:
        results = [i for i in results if i["commune_code"] == int(commune_code)]

    if village_code:
        results = [i for i in results if str(i["village_code"]) == str(village_code)]

    # ======================
    # PAGINATION
    # ======================
    total_items = len(results)
    total_pages = math.ceil(total_items / page_size)

    start = (page - 1) * page_size
    end = start + page_size

    paginated_results = results[start:end]

    # ======================
    # RESPONSE
    # ======================
    return JsonResponse({
        "counts": len(results),
        "count": len(paginated_results),
        "total_items": total_items,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": paginated_results
    })


def get_districts(request, province_code):
    data = load_data()
    districts = {
        item["district_code"]: {
            "code": item["district_code"],
            "name_en": item["district_en"],
            "name_kh": item["district_kh"]
        }
        for item in data if item["province_code"] == province_code
    }
    return JsonResponse(list(districts.values()), safe=False)


def get_provinces(request):
    data = load_data()
    provinces = {
        item["province_code"]: {
            "code": item["province_code"],
            "name_en": item["province_en"],
            "name_kh": item["province_kh"]
        }
        for item in data
    }
    return JsonResponse(list(provinces.values()), safe=False)


def paginate(data, page, page_size):
    total = len(data)
    total_pages = math.ceil(total / page_size)

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "total_items": total,
        "total_pages": total_pages,
        "results": data[start:end]
    }
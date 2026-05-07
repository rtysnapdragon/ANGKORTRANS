from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Country, Province, District, Commune, Village, AdminAddress
from .serializers import (
    CountrySerializer, ProvinceSerializer, DistrictSerializer,
    CommuneSerializer, VillageSerializer, AdminAddressSerializer
)


# ====================== COUNTRY ======================
@api_view(['POST'])
def country_list(request):
    countries = Country.objects.filter(IS_ACTIVE=True)
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def country_create(request):
    serializer = CountrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(CREATED_BY=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def country_update(request, pk):
    country = get_object_or_404(Country, pk=pk)
    serializer = CountrySerializer(country, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(UPDATED_BY=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    return Response({"Message": "Country deleted successfully"})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import District, Commune, Village
from .serializers import DistrictSerializer, CommuneSerializer, VillageSerializer


# ====================== DISTRICT ======================
@api_view(['POST'])
def district_list(request):
    districts = District.objects.all().order_by('DISTRICT_NAME_EN')
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def district_create(request):
    serializer = DistrictSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(CREATED_BY=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def district_update(request, pk):
    district = get_object_or_404(District, pk=pk)
    serializer = DistrictSerializer(district, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(UPDATED_BY=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def district_delete(request, pk):
    district = get_object_or_404(District, pk=pk)
    district.delete()
    return Response({"Message": "District deleted successfully"}, status=status.HTTP_200_OK)


# ====================== COMMUNE ======================
@api_view(['POST'])
def commune_list(request):
    communes = Commune.objects.all().order_by('COMMUNE_NAME_EN')
    serializer = CommuneSerializer(communes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def commune_create(request):
    serializer = CommuneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(CREATED_BY=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def commune_update(request, pk):
    commune = get_object_or_404(Commune, pk=pk)
    serializer = CommuneSerializer(commune, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(UPDATED_BY=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def commune_delete(request, pk):
    commune = get_object_or_404(Commune, pk=pk)
    commune.delete()
    return Response({"Message": "Commune deleted successfully"}, status=status.HTTP_200_OK)


# ====================== VILLAGE ======================
@api_view(['POST'])
def village_list(request):
    villages = Village.objects.all().order_by('VILLAGE_NAME_KH')
    serializer = VillageSerializer(villages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def village_create(request):
    serializer = VillageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(CREATED_BY=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def village_update(request, pk):
    village = get_object_or_404(Village, pk=pk)
    serializer = VillageSerializer(village, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(UPDATED_BY=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def village_delete(request, pk):
    village = get_object_or_404(Village, pk=pk)
    village.delete()
    return Response({"Message": "Village deleted successfully"}, status=status.HTTP_200_OK)

    
# ====================== ADMIN ADDRESS ======================
@api_view(['POST'])
def admin_address_list(request):
    addresses = AdminAddress.objects.all().order_by('-CREATED_AT')
    serializer = AdminAddressSerializer(addresses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def admin_address_create(request):
    serializer = AdminAddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(CREATED_BY=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def admin_address_update(request, pk):
    address = get_object_or_404(AdminAddress, pk=pk)
    serializer = AdminAddressSerializer(address, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(UPDATED_BY=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def admin_address_delete(request, pk):
    address = get_object_or_404(AdminAddress, pk=pk)
    address.delete()
    return Response({"Message": "Address deleted successfully"})
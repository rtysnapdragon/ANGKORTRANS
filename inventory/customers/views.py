from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404
from inventory.suppliers.models import Supplier
from .models import Customer
from .serializers import (
    CustomerSerializer
)


class CustomerModelViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that forces:
    - List     → POST
    - Update   → POST
    - Delete   → GET
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Override list to accept only POST"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Override update to use POST instead of PUT/PATCH"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Override destroy to respond to GET (delete via GET)"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(CREATED_BY=self.request.user)

    def perform_update(self, serializer):
        serializer.save(UPDATED_BY=self.request.user)


# ====================== SPECIFIC VIEWSETS ======================
class CustomerViewSet(CustomerModelViewSet):
    queryset = Customer.objects.all().order_by('-CREATED_AT')
    serializer_class = CustomerSerializer

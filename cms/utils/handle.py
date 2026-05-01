from django.db.models import QuerySet
from rest_framework.request import Request
from django.core.exceptions import FieldError

def build_filter(queryset: QuerySet, request_data: dict, allowed_filters: list = None, filter_mappings: dict = None) -> QuerySet:
    """
    Apply filters to a Django QuerySet based on client request data (e.g., JSON body).
    
    Args:
        queryset (QuerySet): The initial Django QuerySet.
        request_data (dict): The request data containing filter parameters.
        allowed_filters (list, optional): List of keys from request_data that are allowed to be used as filters.
            If None, all valid model fields passed in request_data will be applied.
        filter_mappings (dict, optional): Mapping of request keys to Django ORM lookup parameters.
            e.g., {'gallery_id': 'gallery__id', 'search': 'title__icontains'}
            
    Returns:
        QuerySet: The filtered QuerySet.
    """
    if not request_data or not isinstance(request_data, dict):
        return queryset

    filters = {}
    filter_mappings = filter_mappings or {}
    
    # Exclude common pagination/sorting/misc params from automatic filtering
    exclude_keys = ['page', 'limit', 'offset', 'sort', 'order_by', 'search', 'query']

    for key, value in request_data.items():
        # Skip empty values but allow boolean False
        if value is None or value == '':
            continue
            
        if key in exclude_keys and key not in filter_mappings:
            continue
            
        if allowed_filters is not None and key not in allowed_filters:
            continue

        # Determine the ORM lookup key
        orm_lookup = filter_mappings.get(key, key)
        
        # Auto-handle lists with __in if an exact lookup is implied
        if isinstance(value, list) and not orm_lookup.endswith('__in'):
            orm_lookup = f"{orm_lookup}__in"
            
        filters[orm_lookup] = value

    if filters:
        # We use a try-except block to gracefully handle keys that do not match model fields
        try:
            return queryset.filter(**filters).distinct()
        except FieldError:
            # If a field error occurs (e.g., client sends a key that is not a model field),
            # we isolate valid filters by testing them one by one.
            valid_filters = {}
            for k, v in filters.items():
                try:
                    queryset.filter(**{k: v})
                    valid_filters[k] = v
                except FieldError:
                    pass # Ignore invalid filter keys
                    
            if valid_filters:
                return queryset.filter(**valid_filters).distinct()
            
    return queryset

def get_filters_from_request(request: Request) -> dict:
    """
    Extracts potential filter data from request (query_params or body data).
    Body data takes precedence over query params if keys overlap.
    """
    data = {}
    
    # Get from query params (GET)
    if hasattr(request, 'query_params'):
        for k, v in request.query_params.items():
            # Handle multiple values for the same key as a list
            val_list = request.query_params.getlist(k)
            data[k] = val_list if len(val_list) > 1 else v
    elif hasattr(request, 'GET'):
        for k, v in request.GET.items():
            val_list = request.GET.getlist(k)
            data[k] = val_list if len(val_list) > 1 else v
            
    # Get from body (POST/PUT/etc)
    if hasattr(request, 'data') and isinstance(request.data, dict):
        data.update(request.data)
        
    return data

def apply_request_filters(queryset: QuerySet, request: Request, allowed_filters: list = None, filter_mappings: dict = None) -> QuerySet:
    """
    Extracts filter data from the request and applies it to the given queryset.
    
    Example Usage in a View:
        queryset = Artwork.objects.all()
        # If client sends JSON: {"artist_id": 5, "category_id": [1, 2], "is_public": true}
        filtered_qs = apply_request_filters(queryset, request)
    """
    request_data = get_filters_from_request(request)
    return build_filter(queryset, request_data, allowed_filters, filter_mappings)
from django.contrib.auth.models import Group
from restaurant_app.models import Cart
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ValidationError, FieldError
import logging


def manage_user_group(user, group_name, add=True):
    group = Group.objects.get(name=group_name)
    if add:
        user.groups.add(group)
    else:
        user.groups.remove(group)
    user.save() 

logger = logging.getLogger(__name__)

def apply_filters_and_pagination(queryset, request, filter_mappings=None):
    
    
    filter_dict = {}
    
    # Retrive and apply filters based on provided mappings
    if filter_mappings:
        for model_field, query_param in filter_mappings.items():
            filter_value = request.query_params.get(query_param)
            if filter_value:
                filter_dict[model_field] = filter_value
                
    # Retrieve sorting and pagination parameters
    ordering = request.query_params.get('ordering')
    per_page = request.query_params.get('perpage', default=20)
    page = request.query_params.get('page', default=1)

    try:
        # if filtering_by_date:
        #     queryset = queryset.filter(date=filtering_by_date)
        # if filtering_by_status:
        #     queryset = queryset.filter(status=filtering_by_status)
        if filter_dict:
            queryset = queryset.filter(**filter_dict)
        if ordering:
            sorting_fields = ordering.split(",")
            queryset = queryset.order_by(*sorting_fields)

    except ValidationError as e:
        logger.error(f"ValidationError occurred: {e}")
    except FieldError as e:
        logger.error(f"FieldError occurred: {e}")

    paginator = Paginator(queryset, per_page=per_page)
    try:
        queryset = paginator.page(number=page)
    except EmptyPage:
        queryset = []

    return queryset
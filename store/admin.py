from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import *
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models.aggregates import Count
from . import models

from typing import Any, Optional  # Add Optional

class PriceFilter(admin.SimpleListFilter):
    title = 'Price'
    parameter_name = 'price'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<500000', 'less than 500000'),
            ('>500000', 'more than 500000'),
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> Optional[QuerySet[Any]]:
        if self.value() == '<500000':
            return queryset.filter(price__lt=500000)
        elif self.value() == '>500000':
            return queryset.filter(price__gt=500000)

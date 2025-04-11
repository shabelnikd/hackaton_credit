from django_filters import rest_framework as filters
from .models import Loan


class TenderFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="user", lookup_expr='icontains')

    class Meta:
        model = Loan
        fields = ['search']

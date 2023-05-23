import django_filters
from .models import *
from django_filters import DateFilter, CharFilter, filters
from django import forms

class OrderFilter(django_filters.FilterSet):
    """
    Filter for orders based on various criteria.
    """
    start_date = DateFilter(
        field_name='date_created',
        lookup_expr='gte',
        label='Start Date',
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )
    end_date = DateFilter(
        field_name='date_created',
        lookup_expr='contains',
        label='End Date',
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )
    
    note = CharFilter(field_name='note', lookup_expr='icontains')
    
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_created']

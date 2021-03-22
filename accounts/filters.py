import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class InspectionFilter(django_filters.FilterSet):

	class Meta:
		model = Inspection
		fields = ['location', 'wtgnumber']
		
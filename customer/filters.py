import django_filters
from owner.models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model=Product
        fields=["product_name","price"]
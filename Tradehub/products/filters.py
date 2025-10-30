import django_filters
from .models import Product


class Producfilter(django_filters.filterset):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category_slug", lookup_expr="iexact")
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = Product
        fields = "__all__"

        def filter_in_stock(self, queryset, name, value):
            if value:
                return queryset.filter(stock_quantity_gt=0)
            return queryset
        
        

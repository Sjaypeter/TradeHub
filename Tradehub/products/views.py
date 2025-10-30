from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class Productviewset(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "created_by").all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["price", "created_at", "name"]

    def perform_create(self, serializer):
        serializer.save(created_by =self.request.user)

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
       
        q = request.query_params.get("q", "")
        qs = self.filter_queryset(self.get_queryset())
        if q:
            qs = qs.filter(name__icontains=q)  # partial match
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    

class CategoryViewSet(viewsets.ModelViewSet):
        
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]
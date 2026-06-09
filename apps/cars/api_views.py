from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS
from django.db.models import Q, Count
from .models import Car, Brand, Category
from .serializers import (
    CarListSerializer, CarDetailSerializer, CarCreateSerializer,
    BrandSerializer, CategorySerializer
)


# ──────────────────────────────────────────────
# Custom permission: read-only for everyone,
# write (POST / PUT / PATCH / DELETE) only for
# Django staff / superusers.
# ──────────────────────────────────────────────
class IsStaffOrReadOnly(BasePermission):
    """
    Allow GET / HEAD / OPTIONS to anyone.
    Require request.user.is_staff for all write methods.
    """
    message = 'Only admin users can perform this action.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


# ──────────────────────────────────────────────
# Car endpoints
# ──────────────────────────────────────────────
class CarListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['title', 'brand__name', 'model', 'location']
    ordering_fields = ['price', 'year', 'created_at', 'views_count']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Car.objects.filter(status='available').select_related('brand', 'category')
        params = self.request.query_params
        brand        = params.get('brand')
        category     = params.get('category')
        fuel_type    = params.get('fuel_type')
        transmission = params.get('transmission')
        min_price    = params.get('min_price')
        max_price    = params.get('max_price')
        min_year     = params.get('min_year')
        max_year     = params.get('max_year')
        if brand:        qs = qs.filter(brand__slug=brand)
        if category:     qs = qs.filter(category__slug=category)
        if fuel_type:    qs = qs.filter(fuel_type=fuel_type)
        if transmission: qs = qs.filter(transmission=transmission)
        if min_price:    qs = qs.filter(price__gte=min_price)
        if max_price:    qs = qs.filter(price__lte=max_price)
        if min_year:     qs = qs.filter(year__gte=min_year)
        if max_year:     qs = qs.filter(year__lte=max_year)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarCreateSerializer
        return CarListSerializer


class CarRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CarCreateSerializer
        return CarDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# ──────────────────────────────────────────────
# Brand endpoints
# ──────────────────────────────────────────────
class BrandListCreateAPIView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class BrandRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsStaffOrReadOnly]


# ──────────────────────────────────────────────
# Category endpoints
# ──────────────────────────────────────────────
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


# ──────────────────────────────────────────────
# Stats endpoint  (read-only, public)
# ──────────────────────────────────────────────
class StatsAPIView(APIView):
    def get(self, request):
        data = {
            'total_cars': Car.objects.count(),
            'available_cars': Car.objects.filter(status='available').count(),
            'sold_cars': Car.objects.filter(status='sold').count(),
            'total_brands': Brand.objects.count(),
            'total_categories': Category.objects.count(),
            'top_brands': list(
                Brand.objects.annotate(car_count=Count('cars'))
                .order_by('-car_count')[:5]
                .values('name', 'car_count')
            ),
        }
        return Response(data)

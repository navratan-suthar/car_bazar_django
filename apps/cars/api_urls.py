from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('cars/', api_views.CarListCreateAPIView.as_view(), name='car-list'),
    path('cars/<int:pk>/', api_views.CarRetrieveUpdateDestroyAPIView.as_view(), name='car-detail'),
    path('brands/', api_views.BrandListCreateAPIView.as_view(), name='brand-list'),
    path('brands/<int:pk>/', api_views.BrandRetrieveDestroyAPIView.as_view(), name='brand-detail'),
    path('categories/', api_views.CategoryListCreateAPIView.as_view(), name='category-list'),
    path('stats/', api_views.StatsAPIView.as_view(), name='stats'),
]

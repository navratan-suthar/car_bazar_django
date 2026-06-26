from django.urls import path
from . import views


app_name = 'cars'


urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='list'),
    path('cars/<int:pk>/', views.car_detail, name='detail'),
    path('cars/new/', views.car_create, name='create'),
    path('cars/<int:pk>/edit/', views.car_update, name='update'),
    path('cars/<int:pk>/delete/', views.car_delete, name='delete'),
    path('cars/image/<int:pk>/delete/', views.car_image_delete, name='image_delete'),
    path('brand/<slug:slug>/', views.brand_cars, name='brand_cars'),
    path('category/<slug:slug>/', views.category_cars, name='category_cars'),
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/cars/', views.dashboard_cars, name='dashboard_cars'),
    path('dashboard/brands/', views.dashboard_brands, name='dashboard_brands'),
    path('dashboard/brands/<int:pk>/delete/', views.dashboard_brand_delete, name='dashboard_brand_delete'),
    path('dashboard/categories/', views.dashboard_categories, name='dashboard_categories'),
    path('dashboard/categories/<int:pk>/delete/', views.dashboard_category_delete, name='dashboard_category_delete'),
    path('dashboard/cars/<int:pk>/approve/', views.approve_car, name='approve_car'),
    path('dashboard/cars/<int:pk>/reject/', views.reject_car, name='reject_car'),
    
]

from rest_framework import serializers
from .models import Car, Brand, Category, CarImage


class BrandSerializer(serializers.ModelSerializer):
    car_count = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'car_count', 'created_at']

    def get_car_count(self, obj):
        return obj.cars.filter(status='available').count()


class CategorySerializer(serializers.ModelSerializer):
    car_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'car_count']

    def get_car_count(self, obj):
        return obj.cars.filter(status='available').count()


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'caption', 'order']


class CarListSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    formatted_price = serializers.ReadOnlyField()
    formatted_mileage = serializers.ReadOnlyField()

    class Meta:
        model = Car
        fields = [
            'id', 'title', 'brand', 'brand_name', 'category', 'category_name',
            'model', 'year', 'fuel_type', 'transmission', 'mileage',
            'formatted_mileage', 'price', 'formatted_price', 'location',
            'main_image', 'status', 'is_featured', 'views_count', 'created_at'
        ]


class CarDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = CarImageSerializer(many=True, read_only=True)
    formatted_price = serializers.ReadOnlyField()
    formatted_mileage = serializers.ReadOnlyField()

    class Meta:
        model = Car
        fields = [
            'id', 'title', 'brand', 'category', 'model', 'year',
            'fuel_type', 'transmission', 'mileage', 'formatted_mileage',
            'price', 'formatted_price', 'description', 'location',
            'main_image', 'images', 'status', 'is_featured',
            'contact_phone', 'contact_email', 'views_count',
            'created_at', 'updated_at'
        ]


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'title', 'brand', 'category', 'model', 'year',
            'fuel_type', 'transmission', 'mileage', 'price',
            'description', 'location', 'main_image',
            'contact_phone', 'contact_email', 'status'
        ]

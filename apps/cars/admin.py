from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Category, Car, CarImage


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'car_count', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['logo_preview']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;"/>', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'

    def car_count(self, obj):
        return obj.cars.count()
    car_count.short_description = 'Cars'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'car_count', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def car_count(self, obj):
        return obj.cars.count()
    car_count.short_description = 'Cars'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'year', 'price', 'fuel_type', 'status', 'is_featured', 'views_count', 'created_at']
    list_filter = ['status', 'fuel_type', 'transmission', 'brand', 'is_featured', 'year']
    search_fields = ['title', 'model', 'location', 'description']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'main_image_preview']
    inlines = [CarImageInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'brand', 'category', 'model', 'year', 'status', 'is_featured')
        }),
        ('Details', {
            'fields': ('fuel_type', 'transmission', 'mileage', 'price', 'location')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Images', {
            'fields': ('main_image', 'main_image_preview')
        }),
        ('Contact', {
            'fields': ('contact_phone', 'contact_email')
        }),
        ('Stats', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height:200px;"/>', obj.main_image.url)
        return '-'
    main_image_preview.short_description = 'Preview'


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'image_preview', 'caption', 'order']
    list_filter = ['car__brand']
    search_fields = ['car__title', 'caption']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;"/>', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'

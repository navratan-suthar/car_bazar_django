from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from cloudinary.models import CloudinaryField

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cars:brand_cars', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class e.g. bi-car-front')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


FUEL_CHOICES = [
    ('petrol', 'Petrol'),
    ('diesel', 'Diesel'),
    ('electric', 'Electric'),
    ('hybrid', 'Hybrid'),
    ('cng', 'CNG'),
    ('lpg', 'LPG'),
]

TRANSMISSION_CHOICES = [
    ('manual', 'Manual'),
    ('automatic', 'Automatic'),
    ('cvt', 'CVT'),
    ('dct', 'DCT'),
]

STATUS_CHOICES = [
    ('available', 'Available'),
    ('sold', 'Sold'),
    ('pending', 'Pending Review'),
]


class Car(models.Model):
    title = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual')
    mileage = models.PositiveIntegerField(help_text='Mileage in km')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    location = models.CharField(max_length=200)
    main_image = models.ImageField(upload_to='cars/main/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return f"{self.title} ({self.year})"

    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'pk': self.pk})

    @property
    def formatted_price(self):
        if self.price >= 10000000:
            return f'₹{self.price / 10000000:.2f} Cr'
        elif self.price >= 100000:
            return f'₹{self.price / 100000:.2f} L'
        else:
            return f'₹{self.price:,.0f}'

    @property
    def formatted_mileage(self):
        return f'{self.mileage:,} km'


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Car Image'
        verbose_name_plural = 'Car Images'

    def __str__(self):
        return f'Image for {self.car.title}'

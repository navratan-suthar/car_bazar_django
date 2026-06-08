from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Car, Brand, Category, CarImage
from .forms import CarForm, CarImageForm, CarSearchForm, BrandForm, CategoryForm


def home(request):
    featured_cars = Car.objects.filter(status='available', is_featured=True).select_related('brand')[:6]
    recent_cars = Car.objects.filter(status='available').select_related('brand')[:8]
    brands = Brand.objects.all()
    categories = Category.objects.all()
    total_cars = Car.objects.filter(status='available').count()
    total_brands = Brand.objects.count()
    context = {
        'featured_cars': featured_cars,
        'recent_cars': recent_cars,
        'brands': brands,
        'categories': categories,
        'total_cars': total_cars,
        'total_brands': total_brands,
        'search_form': CarSearchForm(),
    }
    return render(request, 'home.html', context)


def car_list(request):
    cars = Car.objects.filter(status='available').select_related('brand', 'category')
    form = CarSearchForm(request.GET)

    if form.is_valid():
        q = form.cleaned_data.get('q')
        brand = form.cleaned_data.get('brand')
        category = form.cleaned_data.get('category')
        fuel_type = form.cleaned_data.get('fuel_type')
        transmission = form.cleaned_data.get('transmission')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        min_year = form.cleaned_data.get('min_year')
        max_year = form.cleaned_data.get('max_year')
        ordering = form.cleaned_data.get('ordering') or '-created_at'

        if q:
            cars = cars.filter(
                Q(title__icontains=q) |
                Q(brand__name__icontains=q) |
                Q(model__icontains=q) |
                Q(location__icontains=q) |
                Q(description__icontains=q)
            )
        if brand:
            cars = cars.filter(brand=brand)
        if category:
            cars = cars.filter(category=category)
        if fuel_type:
            cars = cars.filter(fuel_type=fuel_type)
        if transmission:
            cars = cars.filter(transmission=transmission)
        if min_price:
            cars = cars.filter(price__gte=min_price)
        if max_price:
            cars = cars.filter(price__lte=max_price)
        if min_year:
            cars = cars.filter(year__gte=min_year)
        if max_year:
            cars = cars.filter(year__lte=max_year)
        cars = cars.order_by(ordering)

    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'total_results': cars.count(),
    }
    return render(request, 'cars/list.html', context)


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.views_count += 1
    car.save(update_fields=['views_count'])
    gallery = car.images.all()
    related_cars = Car.objects.filter(
        brand=car.brand, status='available'
    ).exclude(pk=car.pk)[:4]
    context = {
        'car': car,
        'gallery': gallery,
        'related_cars': related_cars,
    }
    return render(request, 'cars/detail.html', context)


@staff_member_required
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        image_form = CarImageForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            files = request.FILES.getlist('images')
            for i, f in enumerate(files):
                CarImage.objects.create(car=car, image=f, order=i)
            messages.success(request, f'Car listing "{car.title}" created successfully!')
            return redirect('cars:detail', pk=car.pk)
    else:
        form = CarForm()
        image_form = CarImageForm()
    return render(request, 'cars/create.html', {'form': form, 'image_form': image_form})


@staff_member_required
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save()
            files = request.FILES.getlist('images')
            for i, f in enumerate(files):
                CarImage.objects.create(car=car, image=f, order=i)
            messages.success(request, f'Car listing "{car.title}" updated successfully!')
            return redirect('cars:detail', pk=car.pk)
    else:
        form = CarForm(instance=car)
    image_form = CarImageForm()
    return render(request, 'cars/update.html', {'form': form, 'car': car, 'image_form': image_form})


@staff_member_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        title = car.title
        car.delete()
        messages.success(request, f'Car listing "{title}" deleted successfully!')
        return redirect('cars:list')
    return render(request, 'cars/confirm_delete.html', {'car': car})


@staff_member_required
def car_image_delete(request, pk):
    image = get_object_or_404(CarImage, pk=pk)
    car_pk = image.car.pk
    if request.method == 'POST':
        image.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
    return redirect('cars:update', pk=car_pk)


def brand_cars(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    cars = Car.objects.filter(brand=brand, status='available').select_related('brand')
    paginator = Paginator(cars, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'cars/brand_cars.html', {'brand': brand, 'page_obj': page_obj})


def category_cars(request, slug):
    category = get_object_or_404(Category, slug=slug)
    cars = Car.objects.filter(category=category, status='available').select_related('brand')
    paginator = Paginator(cars, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'cars/category_cars.html', {'category': category, 'page_obj': page_obj})


# Dashboard views
@staff_member_required
def dashboard(request):
    from django.db.models import Count
    total_cars = Car.objects.count()
    available_cars = Car.objects.filter(status='available').count()
    sold_cars = Car.objects.filter(status='sold').count()
    pending_cars = Car.objects.filter(status='pending').count()
    total_brands = Brand.objects.count()
    total_categories = Category.objects.count()
    recent_cars = Car.objects.select_related('brand').order_by('-created_at')[:10]
    brand_stats = Brand.objects.annotate(car_count=Count('cars')).order_by('-car_count')[:5]
    context = {
        'total_cars': total_cars,
        'available_cars': available_cars,
        'sold_cars': sold_cars,
        'pending_cars': pending_cars,
        'total_brands': total_brands,
        'total_categories': total_categories,
        'recent_cars': recent_cars,
        'brand_stats': brand_stats,
    }
    return render(request, 'dashboard/index.html', context)


@staff_member_required
def dashboard_cars(request):
    cars = Car.objects.select_related('brand', 'category').order_by('-created_at')
    q = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    if q:
        cars = cars.filter(Q(title__icontains=q) | Q(brand__name__icontains=q))
    if status_filter:
        cars = cars.filter(status=status_filter)
    paginator = Paginator(cars, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/cars.html', {'page_obj': page_obj, 'q': q, 'status_filter': status_filter})


@staff_member_required
def dashboard_brands(request):
    brands = Brand.objects.all().order_by('name')
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added successfully!')
            return redirect('cars:dashboard_brands')
    else:
        form = BrandForm()
    return render(request, 'dashboard/brands.html', {'brands': brands, 'form': form})


@staff_member_required
def dashboard_brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, 'Brand deleted.')
    return redirect('cars:dashboard_brands')


@staff_member_required
def dashboard_categories(request):
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added!')
            return redirect('cars:dashboard_categories')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/categories.html', {'categories': categories, 'form': form})


@staff_member_required
def dashboard_category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted.')
    return redirect('cars:dashboard_categories')


@staff_member_required
def approve_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.status = 'available'
        car.save(update_fields=['status'])
        messages.success(request, f'Car "{car.title}" approved.')
    return redirect('cars:dashboard_cars')


@staff_member_required
def reject_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.status = 'pending'
        car.save(update_fields=['status'])
        messages.warning(request, f'Car "{car.title}" set to pending.')
    return redirect('cars:dashboard_cars')

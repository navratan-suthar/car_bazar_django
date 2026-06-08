from .models import Car, Brand, Category


def car_stats(request):
    return {
        'total_cars': Car.objects.filter(status='available').count(),
        'total_brands': Brand.objects.count(),
        'all_brands': Brand.objects.all(),
        'all_categories': Category.objects.all(),
    }

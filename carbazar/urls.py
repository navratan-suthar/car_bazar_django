from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.sitemaps.views import sitemap
from apps.cars.sitemap import StaticViewSitemap
sitemaps = {
    "static": StaticViewSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
     # Sitemap
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('', include('apps.cars.urls', namespace='cars')),
    path('api/', include('apps.cars.api_urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

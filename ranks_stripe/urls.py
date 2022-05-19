from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('apps.items.urls')),
    path('v2/', include('apps.cart.urls')),
]

if settings.DEBUG:
    if settings.STATIC_ROOT:
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)

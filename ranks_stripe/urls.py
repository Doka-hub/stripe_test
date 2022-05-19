from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('apps.items.urls')),
    path('v2/', include('apps.cart.urls')),
]

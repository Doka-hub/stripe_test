from django.urls import path

# local imports
from .views import (
    ItemDetailView, CheckoutCreateView
)


app_name = 'items'

urlpatterns = [
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('buy/<int:pk>/', CheckoutCreateView.as_view(), name='checkout-create')
]

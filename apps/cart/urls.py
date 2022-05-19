from django.urls import path

# local imports
from .views import (
    ItemListView,
    OrderStatusTemplateView,
    OrderStatusCheckAjaxView,
    OrderDetailView,

    CartItemAddAjaxView,
    CartItemRemoveAjaxView,
    CartOrderAjaxView
)


app_name = 'cart'

urlpatterns = [
    path('item/list/', ItemListView.as_view(), name='item-list'),

    path('order/status/', OrderStatusTemplateView.as_view(),
         name='order-status'),
    path('order/status/check/', OrderStatusCheckAjaxView.as_view(),
         name='order-status-check'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('cart/add/', CartItemAddAjaxView.as_view(), name='cart-add'),
    path('cart/remove/', CartItemRemoveAjaxView.as_view(), name='cart-remove'),
    path('cart/order/', CartOrderAjaxView.as_view(), name='cart-order'),
]

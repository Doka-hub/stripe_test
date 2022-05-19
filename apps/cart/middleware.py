from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

# local imports
from .cart import Cart


class CartMiddleware(MiddlewareMixin):
    def process_view(self, request, func, *args, **kwargs):
        cart = Cart(request)
        request.cart = cart

    def process_template_response(self, request, response):
        cart = Cart(request)
        response.context_data['cart'] = cart
        return response


class StripeMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        response.context_data['stripe_pk'] = settings.STRIPE_PUBLIC_KEY
        return response

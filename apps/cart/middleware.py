from django.utils.deprecation import MiddlewareMixin

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

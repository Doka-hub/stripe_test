from django.http.response import JsonResponse
from django.views.generic import DetailView

# local imports
from apps.cart.stripe import Stripe

from .models import Item


class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/checkout.html'


class CheckoutCreateView(DetailView):
    model = Item
    template_name = 'items/checkout.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        session = Stripe.create_checkout_session(
            **{
                'name': self.object.name,
                'quantity': 1,
                'unit_amount': self.object.price_unit,
            }
        )
        return JsonResponse(
            {
                'sessionId': session.id
            }, status=200
        )

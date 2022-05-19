from django.views.generic import DetailView, ListView, View, TemplateView
from django.shortcuts import get_object_or_404, reverse

# local imports
from apps.items.models import Item

from .mixins import AjaxMixin
from .models import Order
from .stripe import Stripe


class ItemListView(ListView):
    model = Item
    template_name = 'cart/item-list.html'


class OrderDetailView(DetailView, AjaxMixin):
    model = Order
    template_name = 'cart/checkout.html'

    def post(self, request, *args, **kwargs):
        response = self.get_response()
        self.object = self.get_object()

        self.object.amount = self.object.get_amount()
        self.object.save(update_fields=['amount'])

        payment_intent = Stripe.create_payment_intent(
            **{
                'metadata': {'uuid': self.object.uuid},
                'amount': self.object.get_unit_amount(),
            }
        )

        response['intentSecret'] = payment_intent.client_secret
        response['confirmPaymentUrl'] = reverse('cart:order-status')
        return self.ajax_response(response)


class OrderStatusTemplateView(TemplateView):
    template_name = 'cart/status.html'


class OrderStatusCheckAjaxView(View, AjaxMixin):
    def get(self, request, *args, **kwargs):
        response = self.get_response()
        pi_secret = self.request.GET.get('pi_secret')

        payment_intent = Stripe.retrieve_payment_intent(pi_secret)
        if payment_intent.status == 'succeeded':
            uuid = payment_intent.metadata.get('uuid')

            order = get_object_or_404(Order, uuid=uuid)
            order.ordered = True
            order.save(update_fields=['ordered'])

        response.update({**payment_intent})
        return self.ajax_response(response)


class CartItemAddAjaxView(View, AjaxMixin):
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        response = self.get_response()
        cart = request.cart
        item_id = request.POST.get('itemId')

        item = get_object_or_404(Item, id=item_id)

        cart.add(item_id)

        response['itemId'] = item.id
        response['itemName'] = item.name
        response['itemQuantity'] = cart.get_item_quantity(item_id)
        response['itemAmount'] = cart.get_item_amount(item_id, item.price)
        response['itemDeleteUrl'] = reverse('cart:cart-remove')
        response['cartAmount'] = cart.get_amount()
        response['added'] = True
        return self.ajax_response(response)


class CartItemRemoveAjaxView(View, AjaxMixin):
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = self.get_response()
        cart = request.cart

        item_id = request.POST.get('itemId')
        item = get_object_or_404(Item, id=item_id)

        cart.remove(item_id)

        response['itemId'] = item.id
        response['cartAmount'] = cart.get_amount()
        response['removed'] = True
        return self.ajax_response(response)


class CartOrderAjaxView(View, AjaxMixin):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        response = self.get_response()
        cart = request.cart

        order = cart.order()
        if order is None:
            response['orderCreated'] = False
            status_code = 400
        else:
            response['orderId'] = order.id
            response['orderCreated'] = True
            status_code = 201
        return self.ajax_response(response, status=status_code)


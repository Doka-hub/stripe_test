from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404

# local imports
from apps.items.models import Item

from .models import Order, OrderItem


class Cart:
    def __init__(self, request: WSGIRequest):
        self.request = request
        self.session = self.request.session
        self.cart = self.session.get(settings.CART_SESSION_ID)
        if not self.cart:
            self.cart = self.session[settings.CART_SESSION_ID] = {}

    def add(self, item_id: int):
        if item_id == '':
            return
        item = get_object_or_404(Item, id=item_id)

        if item_id in self.cart:
            self.cart[item_id]['quantity'] += 1
            self.cart[item_id]['amount'] = float(item.price) * self.cart[item_id]['quantity']
        else:
            self.cart[item_id] = {'quantity': 1, 'amount': float(item.price)}
        self.save()

    def remove(self, item_id: int):
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def order(self):
        order_items = []
        for item_id in self.cart:
            item = get_object_or_404(Item, id=item_id)
            quantity = self.cart[item_id]['quantity']

            order_item, created = OrderItem.objects.get_or_create(
                item=item,
                user=self.request.user,
                ordered=False
            )
            order_item.quantity = quantity
            order_item.save(update_fields=['quantity'])

            order_items.append(order_item)
        self.clear()

        if order_items:
            order = Order.objects.create(
                user=self.request.user,
                ordered=False,
            )
            order.items.add(*order_items)
        else:
            order = None
        return order

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def delete(self):
        self.session.clear()

    def get_amount(self):
        amount = 0
        for item_id in self.cart:
            quantity = self.cart[item_id]['quantity']
            item = get_object_or_404(Item, id=item_id)
            amount += item.price * quantity
        return amount

    def get_item_quantity(self, item_id: int):
        cart_item = self.cart.get(item_id)
        return cart_item['quantity']

    def get_item_amount(self, item_id: int, price):
        cart_item = self.cart.get(item_id)
        return price * cart_item['quantity']

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)

        for item in items:
            self.cart[str(item.id)]['item'] = item
        for item in list(self.cart.values())[::-1]:
            if item:
                yield item

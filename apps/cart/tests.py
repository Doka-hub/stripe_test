from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse

# local imports
from apps.items.models import Item

from .models import Order, OrderItem


class OrderTest(TestCase):
    def setUp(self) -> None:
        item_data = {
            'name': 'Shorts',
            'description': 'Black',
            'price': 200
        }
        user_data = {
            'username': 'testUser',
            'password': 'password'
        }

        item = Item.objects.create(**item_data)
        user = User.objects.create_user(**user_data)

        order_item = OrderItem.objects.create(user=user, item=item)

        order = Order.objects.create(user=user)
        order.items.add(order_item)

    def test_order_detail(self):
        order = Order.objects.get(user__username='testUser')

        url = order.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_payment_create(self):
        order = Order.objects.get(user__username='testUser')

        url = order.get_absolute_url()
        response = self.client.post(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)

        self.assertIs(type(data['intentSecret']), str)


class CartTest(TestCase):
    def setUp(self) -> None:
        item_data = {
            'name': 'Shorts',
            'description': 'Black',
            'price': 200
        }
        Item.objects.create(**item_data)

        user_data = {
            'username': 'testUser',
            'password': 'password'
        }
        User.objects.create_user(**user_data)

    def test_item_list(self):
        url = reverse('cart:item-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_cart_add_item(self):
        item = Item.objects.get(name='Shorts')

        url = reverse('cart:cart-add')
        response = self.client.post(url, {'itemId': item.id})
        data = response.json()

        cart = self.client.session.get(settings.CART_SESSION_ID)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['added'])

        self.assertEqual(cart[str(item.id)], {'quantity': 1, 'amount': 200.0})

    def test_cart_remove_item(self):
        # add item to cart
        item = Item.objects.get(name='Shorts')

        url = reverse('cart:cart-add')
        self.client.post(url, {'itemId': item.id})

        # remove item from cart
        url = reverse('cart:cart-remove')
        self.client.post(url, {'itemId': item.id})
        response = self.client.post(url, {'itemId': item.id})
        data = response.json()

        cart = self.client.session.get(settings.CART_SESSION_ID)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['removed'])

        self.assertNotIn(str(item.id), cart)

    def test_cart_order(self):
        self.client.login(username='testUser', password='password')

        # add item to cart
        item = Item.objects.get(name='Shorts')

        url = reverse('cart:cart-add')
        self.client.post(url, {'itemId': item.id})

        # order
        url = reverse('cart:cart-order')
        response = self.client.post(url)
        data = response.json()

        cart = self.client.session.get(settings.CART_SESSION_ID)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['orderCreated'])

        order = Order.objects.get(id=data['orderId'])
        order_item = OrderItem.objects.get(
            user__username='testUser', item=item, ordered=False
        )
        self.assertIn(order_item, order.items.all())

        self.assertIsNone(cart)  # cart should be clean after order created

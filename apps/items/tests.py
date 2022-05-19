from django.test import TestCase
from django.shortcuts import reverse

# local imports
from .models import Item


class ItemTest(TestCase):
    def setUp(self) -> None:
        data = {
            'name': 'T-Shirt',
            'description': 'Black',
            'price': 100
        }
        Item.objects.create(**data)

    def test_item_created(self):
        self.assertIsNotNone(Item.objects.get(name='T-Shirt'))

    def test_item_detail(self):
        item = Item.objects.get(name='T-Shirt')

        url = item.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_checkout_create(self):
        item = Item.objects.get(name='T-Shirt')

        url = reverse('items:checkout-create', args=(item.id,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIs(type(data['sessionId']), str)

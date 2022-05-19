from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from uuid import uuid4

# local imports
from apps.items.models import Item


# class Discount(models.Model):


class Order(models.Model):
    uuid = models.UUIDField(default=uuid4, verbose_name='Идентификатор')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='orders', verbose_name='Покупатель')

    items = models.ManyToManyField('OrderItem', related_name='items',
                                   verbose_name='Товары')

    amount = models.DecimalField(blank=True, null=True,
                                 max_digits=10, decimal_places=2,
                                 verbose_name='Сумма (USD)')

    ordered = models.BooleanField(default=False, verbose_name='Оплачен')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return '%s' % self.uuid

    def get_absolute_url(self):
        return reverse('cart:order-detail', args=(self.id, ))

    def get_amount(self):
        return int(sum((i.get_amount() for i in self.items.all())))
    get_amount.short_description = 'Сумма (USD)'

    def get_unit_amount(self):
        return self.get_amount() * 100

    def items_count(self):
        return self.items.count()
    items_count.short_description = 'Кол-во товаров'


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='order_items',
                             verbose_name='Покупатель')
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='order_items',
                             verbose_name='Товар')

    quantity = models.IntegerField(default=1, verbose_name='Количество')

    ordered = models.BooleanField(default=False, verbose_name='Оплачен')

    class Meta:
        verbose_name = 'Предмет заказа'
        verbose_name_plural = 'Предметы заказа'

    def __str__(self):
        return str(self.item)

    @property
    def price(self):
        return self.item.price

    def get_amount(self, quantity: int = None):
        if quantity is None:
            quantity = self.quantity
        return self.price * quantity

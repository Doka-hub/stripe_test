from django.db import models
from django.shortcuts import reverse


class Item(models.Model):
    CURRENCY_CHOICES = (
        ('usd', 'usd'),
        ('rub', 'rub')
    )

    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена (USD)')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items:item-detail', args=(self.id, ))

    @property
    def price_unit(self):
        return int(self.price * 100)

# Generated by Django 4.0.4 on 2022-05-19 03:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('ordered', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='items.item', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Предмет заказа',
                'verbose_name_plural': 'Предметы заказа',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма (USD)')),
                ('ordered', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('items', models.ManyToManyField(related_name='items', to='cart.orderitem', verbose_name='Товары')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]

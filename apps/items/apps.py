from django.apps import AppConfig
from django.db.utils import OperationalError


class ItemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.items'

    verbose_name = 'Товары'

    def ready(self):
        from .models import Item

        items_data = [
            {
                'name': 'Shorts',
                'description': 'White',
                'price': 200
            },
            {
                'name': 'T-Shirt',
                'description': 'Black',
                'price': 100
            },
            {
                'name': 'Sneakers',
                'description': 'Jordan',
                'price': 500
            },
        ]
        try:
            for item_data in items_data:
                Item.objects.get_or_create(**item_data)
        except OperationalError:
            pass

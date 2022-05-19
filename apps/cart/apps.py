from django.apps import AppConfig
from django.db.utils import OperationalError


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cart'

    verbose_name = 'Корзина'

    def ready(self):
        from django.contrib.auth.models import User

        try:
            if not User.objects.filter(username='admin'):
                User.objects.create_user(
                    username='admin', password='1',
                    is_staff=True, is_superuser=True
                )
        except OperationalError:
            pass

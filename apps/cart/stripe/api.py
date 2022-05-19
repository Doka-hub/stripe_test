from django.conf import settings

from decimal import Decimal

import stripe


class Stripe:
    _stripe = stripe
    _stripe.api_key = settings.STRIPE_SECRET_KEY

    @classmethod
    def create_checkout_session(cls, **data):
        unit_amount: int = data.get('unit_amount')
        quantity: int = data.get('quantity')
        name: str = data.get('name')

        session = cls._stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': name
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': quantity,
            }],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )
        return session

    @classmethod
    def create_payment_intent(cls, **data):
        amount = data.get('amount')
        metadata = data.get('metadata')

        intent = cls._stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            automatic_payment_methods={"enabled": True},
            metadata=metadata,

        )
        return intent

    @classmethod
    def retrieve_payment_intent(cls, id_):
        intent = cls._stripe.PaymentIntent.retrieve(id_)
        return intent

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name: str) -> str:
    """Создаёт продукт в Stripe и возвращает его ID."""
    product = stripe.Product.create(name=name)
    return product['id']


def create_stripe_price(product_id: str, amount: int) -> str:
    """
    Создаёт цену для продукта в Stripe.
    amount передаётся в копейках (рублях * 100).
    Возвращает ID цены.
    """
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,  # переводим в копейки
        currency='rub',
    )
    return price['id']


def create_stripe_session(price_id: str) -> tuple:
    """
    Создаёт сессию оплаты в Stripe.
    Возвращает (session_id, payment_url).
    """
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/payments/success/',
        cancel_url='http://localhost:8000/payments/cancel/',
    )
    return session['id'], session['url']
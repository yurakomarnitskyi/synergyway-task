from celery import shared_task

import os
import requests
from .models import User, Address, CreditCard


@shared_task
def fetch_and_save_next_user():
    users_url = os.environ.get(
        'USERS_API_URL', 'https://jsonplaceholder.typicode.com/users'
    )
    response = requests.get(users_url)
    response.raise_for_status()
    users = response.json()
    existing_usernames = set(User.objects.values_list('username', flat=True))
    for u in users:
        if u['username'] not in existing_usernames:
            user = User.objects.create(
                username=u['username'],
                email=u['email'],
                first_name=u.get('name', '').split()[0],
                last_name=' '.join(u.get('name', '').split()[1:]),
            )
            fetch_and_save_address_for_user(user.id)
            fetch_and_save_credit_card_for_user(user.id)
            break


@shared_task
def fetch_and_save_address_for_user(user_id):
    from .models import User
    import requests

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return
    address_url = os.environ.get(
        'ADDRESS_API_URL', 'https://my.api.mockaroo.com/address.json?key=1354ffd0'
    )
    response = requests.get(address_url)
    if response.status_code != 200:
        return
    data = response.json()
    if not isinstance(data, dict):
        data = data[0]

    Address.objects.filter(user=user).delete()
    Address.objects.create(
        user=user,
        street=data.get('street'),
        city=data.get('city'),
        state=data.get('state'),
        zip_code=data.get('zip_code'),
    )


@shared_task
def fetch_and_save_credit_card_for_user(user_id):
    from .models import User
    import requests

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return
    credit_card_url = os.environ.get(
        'CREDIT_CARD_API_URL',
        'https://my.api.mockaroo.com/credit_cards.json?key=1354ffd0',
    )
    response = requests.get(credit_card_url)
    if response.status_code != 200:
        return
    cards = response.json()
    if not isinstance(cards, dict):
        card = cards[0]

    CreditCard.objects.filter(user=user).delete()

    def safe_date(val):
        from datetime import datetime

        if val and isinstance(val, str):
            try:
                dt = datetime.strptime(val.strip(), '%m/%d/%Y')
                return dt.strftime('%Y-%m-%d')
            except Exception:
                pass
        return '2000-01-01'

    CreditCard.objects.create(
        user=user,
        card_number=card.get('credit_card_number', '')[:16],
        expiration_date=safe_date(card.get('expiration_date')),
        cardholder_name=card.get('cardholder_name', 'Unknown'),
    )

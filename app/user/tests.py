import pytest
from user.models import User, Address, CreditCard
from user.tasks import (
    fetch_and_save_next_user,
    fetch_and_save_address_for_user,
    fetch_and_save_credit_card_for_user,
)


@pytest.mark.django_db
def test_fetch_and_save_next_user_creates_user():
    initial_count = User.objects.count()
    fetch_and_save_next_user()
    assert User.objects.count() == initial_count + 1


@pytest.mark.django_db
def test_fetch_and_save_address_for_user_creates_address():
    user = User.objects.create(username='testuser', email='test@example.com')
    fetch_and_save_address_for_user(user.id)
    assert Address.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_fetch_and_save_credit_card_for_user_creates_card():
    user = User.objects.create(username='testuser2', email='test2@example.com')
    fetch_and_save_credit_card_for_user(user.id)
    assert CreditCard.objects.filter(user=user).exists()

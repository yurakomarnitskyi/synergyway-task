from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state}, {self.zip_code}'


class CreditCard(models.Model):
    user = models.ForeignKey(
        User, related_name='credit_cards', on_delete=models.CASCADE
    )
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cardholder_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.cardholder_name} - {self.card_number[-4:]}'

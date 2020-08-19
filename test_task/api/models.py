from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
import uuid


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Currency(models.Model):
    name = models.CharField(max_length=3, help_text='Available currencies')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    currency_numerator = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                           related_name='numerator')
    currency_denominator = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                             related_name='denominator')
    current_rate = models.FloatField()


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                              blank=True)
    balance = models.FloatField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                 related_name='wallet_currency')

    def __str__(self):
        return f'{self.id}'

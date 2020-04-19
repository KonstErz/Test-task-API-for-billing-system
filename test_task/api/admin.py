from django.contrib import admin
from .models import Currency, ExchangeRate, Wallet


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency_numerator', 'currency_denominator', 'current_rate')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'balance', 'currency')

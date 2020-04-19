from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Currency, Wallet


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, attr):
        if User.objects.filter(email=attr).exists():
            raise serializers.ValidationError('email already exist')

        return attr

    def validate_username(self, attr):
        if User.objects.filter(username=attr).exists():
            raise serializers.ValidationError('username already exist')

        return attr


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class WalletCreationSerializer(serializers.Serializer):
    username = serializers.CharField()
    currency = serializers.CharField()

    def validate_currency(self, attr):
        attr = attr.upper()
        if not Currency.objects.filter(name=attr).exists():
            raise serializers.ValidationError('this currency is not in the system')

        return attr


class WalletDepositSerializer(serializers.Serializer):
    currency = serializers.CharField()
    amount = serializers.FloatField()

    def validate_currency(self, attr):
        attr = attr.upper()
        if not Wallet.objects.filter(currency__name=attr).exists():
            raise serializers.ValidationError('no wallet with this currency')

        return attr

    def validate_amount(self, attr):
        if attr <= 0:
            raise serializers.ValidationError('incorrect amount')

        return attr


class ConversionSerializer(serializers.Serializer):
    first_currency = serializers.CharField()
    second_currency = serializers.CharField()
    amount = serializers.FloatField()

    def validate(self, attrs):
        attrs['first_currency'] = attrs['first_currency'].upper()
        attrs['second_currency'] = attrs['second_currency'].upper()

        if not Wallet.objects.filter(currency__name=attrs['first_currency']).exists():
            raise serializers.ValidationError('no wallet with first currency')
        elif not Wallet.objects.filter(currency__name=attrs['second_currency']).exists():
            raise serializers.ValidationError('no wallet with second currency')
        elif attrs['first_currency'] == attrs['second_currency']:
            raise serializers.ValidationError('currencies in pairs should vary')
        elif attrs['amount'] <= 0:
            raise serializers.ValidationError('incorrect amount')

        return attrs


class TransactionSerializer(serializers.Serializer):
    username = serializers.CharField()
    currency = serializers.CharField()
    my_wallet_currency = serializers.CharField()
    amount = serializers.FloatField()

    def validate(self, attrs):
        attrs['currency'] = attrs['currency'].upper()
        attrs['my_wallet_currency'] = attrs['my_wallet_currency'].upper()

        if not Wallet.objects.filter(owner__username=attrs['username']).exists():
            raise serializers.ValidationError('no wallet with this user')
        elif not Wallet.objects.filter(owner__username=attrs['username'],
                                       currency__name=attrs['currency']).exists():
            raise serializers.ValidationError("the user doesn't have a wallet with this currency")
        elif attrs['amount'] <= 0:
            raise serializers.ValidationError('incorrect amount')

        return attrs

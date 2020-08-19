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

    currency = serializers.CharField(max_length=3)

    def validate_currency(self, attr):
        attr = attr.upper()
        if not Currency.objects.filter(name=attr).exists():
            raise serializers.ValidationError(
                'this currency is not in the system')

        return attr


class WalletDepositSerializer(serializers.Serializer):

    wallet_id = serializers.CharField()
    amount = serializers.FloatField()

    def validate_wallet_id(self, attr):
        if not Wallet.objects.filter(id=attr).exists():
            raise serializers.ValidationError('Wallet not found')

        return attr

    def validate_amount(self, attr):
        if attr <= 0:
            raise serializers.ValidationError('incorrect amount')

        return attr


class ConversionSerializer(serializers.Serializer):

    first_wallet_id = serializers.CharField()
    second_wallet_id = serializers.CharField()
    amount = serializers.FloatField()

    def validate(self, attrs):
        if not Wallet.objects.filter(
                id=attrs['first_wallet_id']).exists():
            raise serializers.ValidationError('Wallet not found (1st id)')
        elif not Wallet.objects.filter(
                id=attrs['second_wallet_id']).exists():
            raise serializers.ValidationError('Wallet not found (2nd id)')
        elif attrs['amount'] <= 0:
            raise serializers.ValidationError('incorrect amount')

        return attrs


class TransactionSerializer(serializers.Serializer):

    username = serializers.CharField()
    currency = serializers.CharField(max_length=3)
    my_wallet_id = serializers.CharField()
    amount = serializers.FloatField()

    def validate(self, attrs):
        attrs['currency'] = attrs['currency'].upper()

        if not Wallet.objects.filter(
                id=attrs['my_wallet_id']).exists():
            raise serializers.ValidationError('Wallet not found (id)')
        elif not Wallet.objects.filter(
                owner__username=attrs['username']).exists():
            raise serializers.ValidationError('no wallet with this user')
        elif not Wallet.objects.filter(
                owner__username=attrs['username'],
                currency__name=attrs['currency']).exists():
            raise serializers.ValidationError(
                "the recipient doesn't have a wallet with this currency")
        elif attrs['amount'] <= 0:
            raise serializers.ValidationError('incorrect amount')

        return attrs

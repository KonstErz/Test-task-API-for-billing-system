from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .serializers import (RegistrationSerializer, LoginSerializer,
                          WalletCreationSerializer, WalletDepositSerializer,
                          ConversionSerializer, TransactionSerializer)
from .models import Currency, ExchangeRate, Wallet


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)

        Token.objects.create(user=user)

        return Response({'user_id': user.id})


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            return Response({'Authorization: Token': user.auth_token.key})
        else:
            return Response({'error': 'username or password invalid'}, 400)


class WalletCreatorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WalletCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(username=request.user).first()
        currency = Currency.objects.filter(name=serializer.validated_data['currency']).first()
        wallet = Wallet.objects.create(owner=user, balance=0, currency=currency)

        return Response({'wallet_id': wallet.id})


class WalletDepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WalletDepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not Wallet.objects.filter(owner=request.user,
                                     currency__name=serializer.validated_data['currency']).exists():
            return Response({'error': "you don't have a wallet with this currency"}, 400)

        wallet = Wallet.objects.filter(owner=request.user,
                                       currency__name=serializer.validated_data['currency']).first()
        wallet.balance += serializer.validated_data['amount']
        wallet.save()

        return Response({'wallet successfully replenished by': request.data['amount']})


class ConversionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConversionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet1 = Wallet.objects.filter(owner=request.user,
                                        currency__name=serializer.validated_data['first_currency']).first()
        wallet2 = Wallet.objects.filter(owner=request.user,
                                        currency__name=serializer.validated_data['second_currency']).first()

        if wallet1.balance < request.data['amount']:
            return Response({'error': 'lack of funds in your wallet'}, 400)

        wallet1.balance -= request.data['amount']

        if ExchangeRate.objects.filter(currency_numerator__name=serializer.validated_data['first_currency'],
                                       currency_denominator__name=serializer.validated_data['second_currency']).exists():
            course = ExchangeRate.objects.filter(currency_numerator__name=serializer.validated_data['first_currency'],
                                                 currency_denominator__name=serializer.validated_data['second_currency']).first()
            wallet2.balance += request.data['amount'] * course.current_rate
        elif ExchangeRate.objects.filter(currency_numerator__name=serializer.validated_data['second_currency'],
                                         currency_denominator__name=serializer.validated_data['first_currency']).exists():
            course = ExchangeRate.objects.filter(currency_numerator__name=serializer.validated_data['second_currency'],
                                                 currency_denominator__name=serializer.validated_data['first_currency']).first()
            wallet2.balance += request.data['amount'] * 1 / course.current_rate

        wallet2.balance = round(wallet2.balance, 2)
        wallet1.save()
        wallet2.save()

        return Response({f'Succes! {wallet2.currency} wallet balance is now': wallet2.balance})


class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sending_wallet = Wallet.objects.filter(owner=request.user,
                                               currency__name=serializer.validated_data['my_wallet_currency']).first()
        receiver_wallet = Wallet.objects.filter(owner__username=serializer.validated_data['username'],
                                                currency__name=serializer.validated_data['currency']).first()

        if sending_wallet is None:
            return Response({'error': "you don't have a wallet with this currency"}, 400)
        elif sending_wallet.balance < request.data['amount']:
            return Response({'error': 'lack of funds in your wallet'}, 400)

        sending_wallet.balance -= request.data['amount']

        if sending_wallet.currency != receiver_wallet.currency:
            if ExchangeRate.objects.filter(currency_numerator__name=serializer.validated_data['my_wallet_currency'],
                                           currency_denominator__name=serializer.validated_data['currency']).exists():
                course = ExchangeRate.objects.filter(currency_numerator__name=serializer.validated_data['my_wallet_currency'],
                                                     currency_denominator__name=serializer.validated_data['currency']).first()
                receiver_wallet.balance += request.data['amount'] * course.current_rate
            elif ExchangeRate.objects.filter(currency_numerator__name=serializer.validated_data['currency'],
                                             currency_denominator__name=serializer.validated_data['my_wallet_currency']).exists():
                course = ExchangeRate.objects.filter(currency_numerator__name=serializer.validated_data['currency'],
                                                     currency_denominator__name=serializer.validated_data['my_wallet_currency']).first()
                receiver_wallet.balance += request.data['amount'] * 1 / course.current_rate
        else:
            receiver_wallet.balance += request.data['amount']

        receiver_wallet.balance = round(receiver_wallet.balance, 2)
        sending_wallet.save()
        receiver_wallet.save()

        return Response({f"Succes! {receiver_wallet.owner}'s wallet balance is replenished at": request.data['amount']})

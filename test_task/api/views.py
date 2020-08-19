from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .serializers import (RegistrationSerializer, LoginSerializer,
                          WalletCreationSerializer, WalletDepositSerializer,
                          ConversionSerializer, TransactionSerializer)
from .models import Currency, Wallet
from .course import course_determinant


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

        return Response({'user_id': user.id}, 201)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)
            return Response({'Authorization: Token': user.auth_token.key}, 200)
        else:
            return Response({'error': 'username or password invalid'}, 400)


class WalletCreatorView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WalletCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(username=request.user).first()
        currency = Currency.objects.filter(
            name=serializer.validated_data['currency']).first()
        wallet = Wallet.objects.create(owner=user,
                                       balance=0,
                                       currency=currency)

        return Response({'wallet_id': wallet.id}, 201)


class WalletDepositView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WalletDepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet = Wallet.objects.filter(
            id=serializer.validated_data['wallet_id']).first()
        amount = serializer.validated_data['amount']

        wallet.balance += amount
        wallet.balance = round(wallet.balance, 2)
        wallet.save()

        context = {
            'wallet successfully replenished by': f'{amount} c.u.'
        }

        return Response(context, 200)


class ConversionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConversionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        wallet1 = Wallet.objects.filter(
            id=serializer.validated_data['first_wallet_id']).first()
        wallet2 = Wallet.objects.filter(
            id=serializer.validated_data['second_wallet_id']).first()

        if wallet1.balance < amount:
            return Response({'error': 'lack of funds in your wallet'}, 400)

        wallet1.balance -= amount

        if wallet1.currency != wallet2.currency:
            course = course_determinant(num=wallet1.currency,
                                        den=wallet2.currency)
            if course is None:
                course = course_determinant(num=wallet2.currency,
                                            den=wallet1.currency)
                wallet2.balance += amount * 1 / course.current_rate
            else:
                wallet2.balance += amount * course.current_rate
        else:
            wallet2.balance += amount

        wallet1.balance = round(wallet1.balance, 2)
        wallet2.balance = round(wallet2.balance, 2)
        wallet1.save()
        wallet2.save()

        context = {
            f'Succes! {wallet2.id} wallet balance is now': wallet2.balance
        }

        return Response(context, 200)


class TransactionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rec_user = serializer.validated_data['username']
        rec_cur = serializer.validated_data['currency']
        send_wal_id = serializer.validated_data['my_wallet_id']
        amount = serializer.validated_data['amount']

        sending_wallet = Wallet.objects.filter(
            id=send_wal_id).first()
        receiver_wallet = Wallet.objects.filter(
            owner__username=rec_user,
            currency__name=rec_cur).first()

        if sending_wallet.balance < amount:
            return Response({'error': 'lack of funds in your wallet'}, 400)

        sending_wallet.balance -= amount

        if sending_wallet.currency != receiver_wallet.currency:
            course = course_determinant(num=sending_wallet.currency,
                                        den=receiver_wallet.currency)
            if course is None:
                course = course_determinant(num=receiver_wallet.currency,
                                            den=sending_wallet.currency)
                receiver_wallet.balance += amount * 1 / course.current_rate
            else:
                receiver_wallet.balance += amount * course.current_rate
        else:
            receiver_wallet.balance += amount

        sending_wallet.balance = round(sending_wallet.balance, 2)
        receiver_wallet.balance = round(receiver_wallet.balance, 2)
        sending_wallet.save()
        receiver_wallet.save()

        context = {
            f"Succes! {receiver_wallet.owner}'s wallet balance is replenished at":
                f'{amount} {sending_wallet.currency}'
        }

        return Response(context, 200)

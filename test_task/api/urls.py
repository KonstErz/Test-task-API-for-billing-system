from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from .views import (RegistrationView, LoginView,
                    WalletCreatorView, WalletDepositView,
                    ConversionView, TransactionView)


urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('walletcreation/', WalletCreatorView.as_view()),
    path('walletdeposit/', WalletDepositView.as_view()),
    path('conversion/', ConversionView.as_view()),
    path('transaction/', TransactionView.as_view()),
]

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (RegistrationView, LoginView,
                    WalletCreatorView, WalletDepositView,
                    ConversionView, TransactionView)


urlpatterns = [
    path('registration/', csrf_exempt(RegistrationView.as_view())),
    path('login/', csrf_exempt(LoginView.as_view())),
    path('walletcreation/', csrf_exempt(WalletCreatorView.as_view())),
    path('walletdeposit/', csrf_exempt(WalletDepositView.as_view())),
    path('conversion/', csrf_exempt(ConversionView.as_view())),
    path('transaction/', csrf_exempt(TransactionView.as_view())),
]

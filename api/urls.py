from django.urls import path
from api.views import (
    GetConnectAccountLink,
    GetBalance,
    MakePayout,
    CreateCheckoutSession,
    Webhook
)

urlpatterns = [
    path("fetch-connect-account-link/", GetConnectAccountLink.as_view()),
    path("fetch-balance/", GetBalance.as_view()),
    path("payout/", MakePayout.as_view()),
    path("webhook/", Webhook.as_view()),
    path("create-checkout-session/", CreateCheckoutSession.as_view()),
]

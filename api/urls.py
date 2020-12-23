from django.urls import path
from api.views import GetConnectAccountLink, GetBalance, CreateCheckoutSession, ConnectedAccountWebhook

urlpatterns = [
    path("fetch-connect-account-link/", GetConnectAccountLink.as_view()),
    path("fetch-balance/", GetBalance.as_view()),
    path("connected-account-webhook/", ConnectedAccountWebhook.as_view()),
    path("create-checkout-session/", CreateCheckoutSession.as_view()),
]

from django.urls import path
from api.views import CreateConnectedAccount, CreateCheckoutSession

urlpatterns = [
    path("create-connected-account/", CreateConnectedAccount.as_view()),
    path("create-checkout-session/", CreateCheckoutSession.as_view()),
]

import stripe
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account
stripe.api_key = 'sk_test_51HuVPWAcBKZyz6L0VrdkpL6x3BXnu7XVEDuA1f3PV22vky75DUp0HY3IxgXbwPNKcmVpzHIdJzv8QHzs73QKgOb100YuP9gb2N'


class CreateConnectedAccount(APIView):
    def post(self, request):
        print("s")
        user = User.objects.get(email="test@test.com")
        account = stripe.Account.create(
            type='express',
        )
        account_obj, _ = Account.objects.get_or_create(
            user=user,
            defaults={"account_id": account.id}
        )
        account_links = stripe.AccountLink.create(
            account=account.id,
            refresh_url='http://localhost:3000/reauth',
            return_url='http://localhost:3000',
            type='account_onboarding',
        )

        return Response({"url": account_links.url})


class CreateCheckoutSession(APIView):
    def post(self, request):
        account = Account.objects.first()
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'name': 'Kavholm rental',
                'amount': 1000,
                'currency': 'usd',
                'quantity': 1,
            }],
            payment_intent_data={
                'application_fee_amount': 123,
                'transfer_data': {
                    'destination': account.account_id,
                },
            },
            success_url='https://example.com/success',
            cancel_url='https://example.com/failure',
        )
        return Response({"checkout_session_id": session.id})

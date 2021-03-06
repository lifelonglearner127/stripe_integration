import stripe
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account
stripe.api_key = 'sk_test_51HuVPWAcBKZyz6L0VrdkpL6x3BXnu7XVEDuA1f3PV22vky75DUp0HY3IxgXbwPNKcmVpzHIdJzv8QHzs73QKgOb100YuP9gb2N'


class GetConnectAccountLink(APIView):
    def post(self, request):
        user = User.objects.get(email="test@test.com")

        connect_account = Account.objects.filter(user=user).first()

        if connect_account:
            if connect_account.enabled:
                login_link = stripe.Account.create_login_link(
                    connect_account.account_id,
                    redirect_url="http://localhost:3000"
                )
                return Response({"url": login_link.url})
            else:
                account_id = connect_account.account_id
        else:
            account = stripe.Account.create(
                type='express',
            )
            Account.objects.create(user=user, account_id=account.id)
            account_id = account.id

        account_links = stripe.AccountLink.create(
            account=account_id,
            refresh_url='http://localhost:3000/reauth',
            return_url='http://localhost:3000',
            type='account_onboarding',
        )

        return Response({"url": account_links.url})


class GetBalance(APIView):
    def get(self, request):
        user = User.objects.get(email="test@test.com")
        balance = stripe.Balance.retrieve(
            stripe_account=user.account.account_id,
        )
        return Response(
            {
                "balanceAvailable": balance.available[0].amount,
                "balancePending": balance.pending[0].amount,
            }
        )
    

class MakePayout(APIView):
    def post(self, request):
        user = User.objects.get(email="test@test.com")
        balance = stripe.Balance.retrieve(
            stripe_account=user.account.account_id,
        )

        print(balance)
        payout = stripe.Payout.create(
            amount=balance.available[0].amount,
            currency=balance.available[0].currency,
            stripe_account=user.account.account_id,
        )
        return Response(status=status.HTTP_200_OK)


class Webhook(APIView):
    def post(self, request):
        # try:
        #     event = stripe.Webhook.construct_event(
        #         payload=request.data,
        #         sig_header=signature,
        #         secret="whsec_dk8OsQJUBnmgzDsjRflgS8V5Bg5LHBNO",
        #     )
        # except ValueError as e:
        #     return Response(status=400)
        # except stripe.error.SignatureVerificationError as e:
        #     return Response(status=400)
        event = request.data
        print(event)
        if event["type"] == "account.updated":
            account = Account.objects.get(account_id=event["data"]["object"]["id"])
            if not account.enabled:
                account.enabled = True
                account.save()

        elif event["type"] == "checkout.session.completed":
            print("session")

        return Response(status=200)


class CreateCheckoutSession(APIView):
    def post(self, request):
        account = Account.objects.first()
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'name': 'Agent Store Product',
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
            success_url='http://localhost:3000',
            cancel_url='https://example.com/failure',
        )
        return Response({"checkout_session_id": session.id})

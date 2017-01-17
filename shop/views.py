from logging import getLogger

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
import stripe

logger = getLogger(__name__)


class ShowCartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/cart.html', {
            'data_key': settings.STRIPE_PUBLISHABLE_KEY,
            'data_amount': 500,  # Amount in cents
            'data_name': 'akiyoko blog',
            'data_description': 'TEST',
        })


class ShowSubscriptionCartView(View):
    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_API_KEY

        # upcoming_invoice = stripe.Invoice.upcoming(customer="")
        """
        invoice_item_result = stripe.InvoiceItem.create(
            customer="",
            amount=2500,
            currency="jpy",
            description="One-time setup fee 使用量に応じて動的に計算",
            subscription='',
            tax_percent=8.0,
        )
        """

        return render(request, 'shop/subscription_cart.html', {
            'data_key': settings.STRIPE_PUBLISHABLE_KEY,
            'data_name': 'hoge 購読従量課金',
            'data_description': 'ディスクリプションあああ',
            'upcoming_invoice': upcoming_invoice,
            'invoice_item_result': invoice_item_result,
        })


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here: https://dashboard.stripe.com/account/apikeys
        stripe.api_key = settings.STRIPE_API_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create a charge: this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=500,  # Amount in cents
                currency='usd',
                source=token,
                description='This is a test.',
            )
        except stripe.error.CardError as e:
            # The card has been declined
            return render(request, 'error.html', {
                'message': "Your payment cannot be completed. The card has been declined.",
            })

        logger.info("Charge[{}] created successfully.".format(charge.id))
        messages.info(request, "Your payment has been completed successfully.")
        return render(request, 'shop/complete.html', {
            'charge': charge,
        })


class SubscribeView(View):
    def post(self, request, *args, **kwargs):
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here: https://dashboard.stripe.com/account/apikeys
        stripe.api_key = settings.STRIPE_API_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create a subscription: this will charge the user's card
        try:
            customer = stripe.Customer.create(
                email=request.POST['stripeEmail'],
                source=request.POST['stripeToken'],
            )
            subscription = stripe.Subscription.create(
                customer=customer.id,
                plan='daily_100',
                quantity=request.POST['my_quantity'],
                tax_percent=8.0,
            )
        except stripe.error.CardError as e:
            # The card has been declined
            return render(request, 'error.html', {
                'message': "Your payment cannot be completed. The card has been declined.",
            })

        logger.info("Subscription[{}] created successfully.".format(subscription.id))
        messages.info(request, "Your subscription has been completed successfully.")
        return render(request, 'shop/complete.html', {
            'charge': subscription,
        })

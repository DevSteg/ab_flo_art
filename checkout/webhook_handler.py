from django.http import HttpResponse
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
import json
import time


class StripeWH_Handler:
    """ Handle Stripe Webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
            Handle a generic/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
            Handle a payment_intent.succeeded webhook event
        """
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in shipping details
        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        # Update profile info if save_info is True
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_full_name_ = shipping_details.name,
                profile.default_phone_number = shipping_details.phone,
                profile.default_street_address1 = shipping_details.address.line1,
                profile.default_street_address2 = shipping_details.address.line2,
                profile.default_town_city = shipping_details.address.city,
                profile.default_postcode = shipping_details.address.postal_code,
                profile.default_county = shipping_details.address.state,
                profile.default_country = shipping_details.address.country,
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    town_city__iexact=shipping_details.address.city,
                    postcode__iexact=shipping_details.address.postal_code,
                    county__iexact=shipping_details.address.state,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} \
                        | SUCCESS: Verified order already in database',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    town_city=shipping_details.address.city,
                    postcode=shipping_details.address.postal_code,
                    county=shipping_details.address.state,
                    country=shipping_details.address.country,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                for item_id, quantity in json.loads(basket).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]} \
                                    | ERROR: {e}', status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} \
                    | SUCCESS: Created order in webhook',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
            Handle a payment_intent.payment_failed webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

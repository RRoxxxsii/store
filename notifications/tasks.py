from celery import shared_task
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

import celery_app
from account.models import Customer
from store.models import Product


@shared_task
def send_email_to_subs(discount_percent: int, product_id: int, price_with_discount: int) -> None:
    """
    Send email message to people subscribed on the listing
    """
    recipients = Customer.objects.filter(on_mail_listing=True)
    email_subject = 'New Product In Stock'
    email_body_template = 'email/new_product_notification.txt'
    print(discount_percent, price_with_discount)
    email_messages = []
    for recipient in recipients:
        user_name = recipient.user_name
        email_body = render_to_string(email_body_template, {
            'user_name': user_name,
            'id': product_id,
            'discount': discount_percent,
            'price_with_discount': price_with_discount
        })

        email_message = (
            email_subject,
            email_body,
            'your-email@example.com',
            [recipient.email],
        )

        email_messages.append(email_message)
    send_mass_mail(email_messages)





from simpleblog.contact.models import Contact
from config.env import env

from django.core.mail import EmailMultiAlternatives

from django.db import transaction
from django.db.models import QuerySet


@transaction.atomic
def contact_create(*, email:str, name:str, content:str) -> QuerySet[Contact]:

    contact = Contact.objects.create(
        email = email,
        name = name,
        content = content,
    )

    send_email(name, content, email)

    return contact

def send_email(name, content, email):
    message = EmailMultiAlternatives(
        name,
        content,
        to=[env('EMAIL_SEND_TO_CONTACT', default='jalal.a.sadeghi@gmail.com')],
        from_email=email,
        reply_to=[email])
    message.send()


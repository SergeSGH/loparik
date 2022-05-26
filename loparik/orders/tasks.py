from django.conf import settings
from django.core.mail import send_mail

from loparik.celery import app


@app.task
def order_created(dest_email, subject, email_text):
    mail_sent = send_mail(
        subject=subject,
        message=email_text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[dest_email, ],
        fail_silently=False
    )
    return mail_sent

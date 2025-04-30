from django.core.mail import EmailMultiAlternatives
import threading
from django.conf import settings
from django.core.mail import EmailMessage
import uuid

def generate_resend_link(token):
    return f"{settings.FRONTEND_URL}/reset-password/?token={token}"


from django.core.mail import EmailMessage


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.content_subtype = "html"
        EmailThread(email).start()
import django_rq
import requests

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class EnqueueBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for message in email_messages:
            message.from_email = "{0} <{1}>".format(settings.CLUB['name'], settings.EMAIL_FROM)
            django_rq.enqueue(mailgun_send, message)

def mailgun_send(message):
    return requests.post(
        "https://api.mailgun.net/v3/{0}/messages".format(settings.MAILGUN_DOMAIN),
        auth=("api", settings.MAILGUN_API_KEY),
        # We do not use the from specified in the message
        # TODO move this to the send_messages method
        data={"from": message.from_email,
              "to": message.to,
              "cc": message.cc,
              "bcc": message.bcc,
              "subject": message.subject,
              "text": message.body, })
    # "html": "<html>HTML version of the body</html>"})

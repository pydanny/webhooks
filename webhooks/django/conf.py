from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

WEBHOOKS_SENDER = getattr(settings, "WEBHOOKS_SENDER", "webhooks.django.senders.sender")
WEBHOOK_EVENTS = getattr(settings, "WEBHOOK_EVENTS", None)


try:
    WEBHOOKS_SENDER_CALLABLE = __import__(WEBHOOKS_SENDER)
except ImportError:
    msg = "Please set an existing WEBHOOKS_SENDER class."
    raise ImproperlyConfigured(msg)

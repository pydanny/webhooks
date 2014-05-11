# -*- coding: utf-8 -*-
"""
Where the hook function/decorator is stored.
Unlike the standard webhooks.decorator, this doesn't
    have the developer specify the exact sender callable.
"""

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

import wrapt


WEBHOOKS_SENDER = getattr(settings, "WEBHOOKS_SENDER", "webhooks.backends.base.SyncSQLSender")

try:
    SenderClass = __import__(WEBHOOKS_SENDER)
except ImportError:
    msg = "Please set an existing WEBHOOKS_SENDER class."
    raise ImproperlyConfigured(msg)


def hook(event):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        """ This should calls the SenderClass, which can be defined by the sender.
            kwargs needs to include an 'creator' key
        """

        sender = SenderClass(
            wrapped,  # function delivering a payload
            event,  # name of the event being called
            kwargs["creator"],  # The model instance representing the creator of this action
            *args,  # Argument list for the wrapped function
            **kwargs  # Kweyword argument list for the wrapped function
        )
        sender.send()

    return wrapper



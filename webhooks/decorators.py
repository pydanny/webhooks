# -*- coding: utf-8 -*-
"""
Where the hook function/decorator is stored
"""
import wrapt

from .exceptions import SenderNotCallable

__all__ = ("hook", "webhook")


def hook(event, sender_callable, hash=True):
    # TODO - make a Django version that avoids the sender argument.

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        """ This should calls the sender_callable.
            kwargs needs to include an 'creator' key
        """

        if not callable(sender_callable):
            raise SenderNotCallable(sender_callable)

        try:
            kwargs["creator"]
        except KeyError:
            raise KeyError("Hooks must include a creator keyword argument")

        ##################################
        # :wrapped: hooked function delivering a payload
        # :event: name of the event being called
        # :args: Argument list for the wrapped function
        # :kwargs: Keyword arguments for the wrapped function. Must include 'creator'

        # Send the hooked function
        status = sender_callable(wrapped, event, *args, **kwargs)

        # Status can be anything:
        #   * The result of a synchronous sender
        #   * A generic status message for asynchronous senders
        #   * 
        return status

    return wrapper


# alias the hook decorator so it's easier to remember the API
webhook = hook

# -*- coding: utf-8 -*-
"""
Where the hook function/decorator is stored
"""
import wrapt


def hook(event, hash=True, sender="webhooks.simple.sender"):
    # TODO - possibly remove sender default

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        """ This should calls the sender_callable.
            kwargs needs to include an 'creator' key
        """

        try:
            creator = kwargs["creator"]
        except KeyError:
            raise KeyError("Hooks must include a creator keyword argument")

        sender_callable = __import__(sender)

        ##################################
        # :wrapped: hooked function delivering a payload
        # :event: name of the event being called
        # :args: Argument list for the wrapped function
        # :kwargs: Keyword arguments for the wrapped function. Must include 'creator'

        # Send the hooked function
        sender_callable.send(wrapped, event, creator, *args, **kwargs)

    return wrapper


# alias the hook decorator so it's easier to remember the API
webhook = hook

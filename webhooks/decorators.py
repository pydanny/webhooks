# -*- coding: utf-8 -*-
"""
Where the hook function/decorator is stored
"""
from functools import partial

import wrapt

from .hashes import basic_hash_function, placebo_hash_function
from .exceptions import SenderNotCallable

__all__ = ("hook", "webhook", "unhashed_hook")


def base_hook(event, sender_callable, hash_function):

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        """ This should calls the sender_callable.
            kwargs needs to include an 'creator' key
        """

        # If sender_callable isn't valid, stop early for easy debugging
        if not callable(sender_callable):
            raise SenderNotCallable(sender_callable)

        # If no creator is passed, stop early for easy debugging
        try:
            kwargs["creator"]
        except KeyError:
            raise KeyError("Hooks must include a creator keyword argument")

        # Call the hash function and save result to a hash_value argument
        kwargs['hash_value'] = hash_function()

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
        #   * Returns the response of the hash_function
        return status

    return wrapper


# This is the hook everyone wants to use
hook = partial(base_hook, hash_function=basic_hash_function)

# alias the hook decorator so it's easier to remember the API
webhook = hook

# This is a hook with a placebo hash function
unhashed_hook = partial(base_hook, hash_function=placebo_hash_function)

# -*- coding: utf-8 -*-
"""
Where the hook function/decorator is stored
"""
from __future__ import absolute_import
from functools import partial

import wrapt

from .hashes import basic_hash_function
from .exceptions import SenderNotCallable

__all__ = ("hook", "webhook", "unhashed_hook")


def base_hook(sender_callable, hash_function, **dkwargs):

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        """ This should calls the sender_callable.
            kwargs needs to include an 'creator' key
        """

        # If sender_callable isn't valid, stop early for easy debugging
        if not callable(sender_callable):
            raise SenderNotCallable(sender_callable)

        # Call the hash function and save result to a hash_value argument
        hash_value = None
        if hash_function is not None:
            hash_value = hash_function()

        ##################################
        # :wrapped: hooked function delivering a payload
        # :dkwargs: name of the event being called
        # :hash_value: hash_value to determine the uniqueness of the payload
        # :args: Argument list for the wrapped function
        # :kwargs: Keyword arguments for the wrapped function. Must include 'creator'

        # Send the hooked function
        status = sender_callable(wrapped, dkwargs, hash_value, *args, **kwargs)

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

# This is a hook with no hash function
unhashed_hook = partial(base_hook, hash_function=None)

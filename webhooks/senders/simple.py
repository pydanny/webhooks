# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .base import Senderable

# First element is 0 to represent the first attempt
ATTEMPTS = [0, 1, 2, 3, 4]


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):

    senderobj = Senderable(
        wrapped, dkwargs, hash_value, ATTEMPTS, *args, **kwargs
    )
    return senderobj.send()


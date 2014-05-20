# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .base import Senderable, value_in

ATTEMPTS = [0, 1, 2, 3]


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):
    senderobj = Senderable(
        wrapped, dkwargs, hash_value, ATTEMPTS, *args, **kwargs
    )

    senderobj.url = value_in("url", dkwargs, kwargs)

    return senderobj.send()

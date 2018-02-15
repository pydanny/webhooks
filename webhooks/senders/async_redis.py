# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .base import Senderable, value_in, value_in_opt

from rq.decorators import job


ATTEMPTS = [0, 1, 2, 3]


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):

    senderobj = Senderable(
        wrapped, dkwargs, hash_value, ATTEMPTS, *args, **kwargs
    )

    senderobj.url = value_in("url", dkwargs, kwargs)
    connection = value_in("connection", dkwargs, kwargs)
    redis_timeout = value_in_opt("redis_timeout", dkwargs, kwargs)

    @job('default', connection=connection, timeout=redis_timeout)
    def worker(senderobj):
        return senderobj.send()

    return worker(senderobj)

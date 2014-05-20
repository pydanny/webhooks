from __future__ import absolute_import

from rq.decorators import job

from .base import Senderable, value_in

ATTEMPTS = [0, 1, 2, 3]


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):

    senderobj = Senderable(
        wrapped, dkwargs, hash_value, ATTEMPTS, *args, **kwargs
    )

    connection = value_in("url", dkwargs, kwargs)
    connection = value_in("connection", dkwargs, kwargs)

    @job('default', connection=connection)
    def worker(senderobj):

        return senderobj.send()

    return worker(senderobj)

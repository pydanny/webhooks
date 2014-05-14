from .base import Senderable

ATTEMPTS = [0, 1, 2, 3]


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):
    senderobj = Senderable(
        wrapped, dkwargs, hash_value, ATTEMPTS, *args, **kwargs
    )

    if "url" in kwargs:
        senderobj.url = kwargs['url']
    elif "url" in dkwargs:
        senderobj.url = dkwargs['url']
    else:
        raise TypeError("sender_targeted needs a URL argument.")

    return senderobj.send()

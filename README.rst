===============================
webhooks
===============================

.. image:: https://pypip.in/d/webhooks/badge.png
        :target: https://pypi.python.org/pypi/webhooks

.. image:: https://badge.fury.io/py/webhooks.png
    :target: https://badge.fury.io/py/webhooks

.. image:: https://travis-ci.org/pydanny/webhooks.png
   :alt: Build Status
   :target: https://travis-ci.org/pydanny/webhooks

.. image:: https://pypip.in/wheel/webhooks/badge.png
    :target: https://pypi.python.org/pypi/webhooks/
    :alt: Wheel Status

Python + Webhooks Made Easy

* Free software: BSD license
* Documentation: http://webhooks.rtfd.org.

**WARNING** This project is in a pre-alpha state. It's not ready for use on ANYTHING.

Python Versions
----------------

Currently works in:

    * Python 2.7
    * Python 3.3

Existing Features
------------------

* Easy to integrate into any package or project
* Comes with several built-in senders for synchronous webhooks.
* Comes with a RedisQ-powered asynchronous webhook.
* Extendable functionality through the use of custom senders and hash functions.

Planned Features
-----------------

* Comes with many built-in senders for synchronous and asynchronous webhooks.
* Special functions for combining multiple sends of identical payloads going to one target into one.
* Follows http://resthooks.org patterns
* Great documentation
* Compatibility with PyPy

Usage
-----

Follow these easy steps:

1. Import the ``webhook`` decorator.
2. Define a function that returns a JSON-serializable dictionary or iterable.
3. Add the ``webhook`` decorator and pass in a ``sender_callable``.
4. Call the function!

Synchronous example (async examples to come soon):

.. code-block:: python

    >>> from webhooks import webhook
    >>> from webhooks.senders import targeted

    >>> @webhook(sender_callable=targeted.sender)
    >>> def basic(url, wife, husband):
    >>>     return {"husband": husband, "wife": wife}

    >>> r = basic(url="http://httpbin.org/post", husband="Danny", wife="Audrey")
    >>> import pprint
    >>> pprint.pprint(r)
    {'attempt': 1,
    'hash': '29788eb987104b8a87d201292fa459d9',
    'husband': 'Danny',
    'response': b'{\n  "args": {},\n  "data": "",\n  "files": {},\n  "form": {\n    "attempt": "1",\n    "hash": "29788eb987104b8a87d201292fa459d9",\n    "husband": "Danny",\n    "url": "http://httpbin.org/post",\n    "wife": "Audrey"\n  },\n  "headers": {\n    "Accept": "*/*",\n    "Accept-Encoding": "gzip, deflate",\n    "Connection": "close",\n    "Content-Length": "109",\n    "Content-Type": "application/x-www-form-urlencoded",\n    "Host": "httpbin.org",\n    "User-Agent": "python-requests/2.3.0 CPython/3.3.5 Darwin/12.3.0",\n    "X-Request-Id": "d25119e4-08ba-4523-abc4-b9a9ac10225b"\n  },\n  "json": null,\n  "origin": "108.185.146.101",\n  "url": "http://httpbin.org/post"\n}',
    'status_code': 200,
    'url': 'http://httpbin.org/post',
    'wife': 'Audrey'}
    


Projects Powered by Webhooks
----------------------------

* https://github.com/pydanny/dj-webhooks

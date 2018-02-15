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

**WARNING** This project is in a beta state. It's still undergoing some changes and documentation is in-progress.

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
4. Define timeout, any custom headers such as authentication, signing_secret, and encoding (application/json|application/x-www-form-urlencoded)
5. Call the function!

Synchronous example (async examples to come soon):

.. code-block:: python

    >>> from webhooks import webhook
    >>> from webhooks.senders import targeted

    >>> @webhook(sender_callable=targeted.sender)
    >>> def basic(wife, husband, url, encoding, timeout, custom_headers, signing_secret):
    >>>     return {"husband": husband, "wife": wife}

    >>> r = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", url="http://httpbin.org/post", encoding="application/json", \
    >>>     timeout=10, custom_headers = {"Basic" : "dXNlcjpzdXBlcnNlY3JldA=="}, signing_secret="secret1")
    >>> import pprint
    >>> pprint.pprint(r)
    {'attempt': 1,
     'error': None,
     'hash': '9d930cc754004d5790869fdfb6064f62',
     'husband': 'Daniel Roy Greenfeld',
     'post_attributes': {'headers': {'Basic': 'dXNlcjpzdXBlcnNlY3JldA==',
                                     'x-hub-signature': 'sha256=e67a669f944fe752f9d9da15c5bcb4d332fceb4940ab512090e124c52c44cfa5'},
                         'json': '{"hash": "9d930cc754004d5790869fdfb6064f62", "husband": "Daniel Roy Greenfeld", "wife": "Audrey Roy Greenfeld"}',
                         'timeout': 10},
     'response': '{\n  "args": {}, \n  "data": "\\"{\\\\\\"hash\\\\\\": \\\\\\"9d930cc754004d5790869fdfb6064f62\\\\\\", \\\\\\"husband\\\\\\": \\\\\\"Daniel Roy Greenfeld\\\\\\", \\\\\\"wife\\\\\\": \\\\\\"Audrey Roy Greenfeld\\\\\\"}\\"", \n  "files": {}, \n  "form": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate", \n    "Basic": "dXNlcjpzdXBlcnNlY3JldA==", \n    "Connection": "close", \n    "Content-Length": "125", \n    "Content-Type": "application/json", \n    "Host": "httpbin.org", \n    "User-Agent": "python-requests/2.18.4", \n    "X-Hub-Signature": "sha256=e67a669f944fe752f9d9da15c5bcb4d332fceb4940ab512090e124c52c44cfa5"\n  }, \n  "json": "{\\"hash\\": \\"9d930cc754004d5790869fdfb6064f62\\", \\"husband\\": \\"Daniel Roy Greenfeld\\", \\"wife\\": \\"Audrey Roy Greenfeld\\"}", \n  "origin": "38.104.237.126", \n  "url": "http://httpbin.org/post"\n}\n',
     'status_code': 200,
     'success': True,
     'wife': 'Audrey Roy Greenfeld'}

    


Projects Powered by Webhooks
----------------------------

* https://github.com/pydanny/dj-webhooks

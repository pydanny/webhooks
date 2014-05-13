===============================
webhooks
===============================

.. image:: https://pypip.in/d/webhooks/badge.png
        :target: https://pypi.python.org/pypi/webhooks

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
    * PyPy

Existing Features
------------------

* Easy to integrate into any package or project
* Comes with several built-in senders for synchronous webhooks.
* Extendable functionality through the use of custom senders and hash functions.

Planned Features
-----------------

* Comes with numerous built-in senders for synchronous and asynchronous webhooks.
* Special functions for combining multiple sends of identical payloads going to one target into one.
* Follows http://resthooks.org patterns
* Great documentation
* Great tests

Usage
-----

Follow these easy steps:

1. Import the ``webhook`` decorator.
2. Define a function that returns a JSON-serializable dictionary or iterable.
3. Add the ``webhook`` decorator and pass in a ``sender_callable``.
4. Call the function!

Synchronous example (async examples to come soon):

.. code-block:: python

    from webhooks import webhook
    from webhooks.senders import targeted

    @webhook(sender_callable=targeted.sender)
    def basic(url, wife, husband):
        return {"husband": husband, "wife": wife}

    basic(url="http://httpbin.org/post", "Danny", "Audrey")
    
Projects Powered by Webhooks
----------------------------

* https://github.com/pydanny/dj-webhooks

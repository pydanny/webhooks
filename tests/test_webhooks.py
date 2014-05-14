#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_webhooks
----------------------------------

Tests for `webhooks` module.
"""


from webhooks import webhook
from webhooks.senders import async_redis


def test_async():

    # First, test the async.worker function
    @webhook(sender_callable=async_redis.worker)
    def worker(url, language):
        return {"language": language, "url": url}

    status = worker(url="http://httpbin.org/post", language="python")

    assert status['language'] == "python"
    assert len(status['hash']) > 10

    # Second, test the sender, which handles the async components
    @webhook(sender_callable=async_redis.sender)
    def sender(url, language):
        return {"language": language, "url": url}

    sender(url="http://httpbin.org/post", language="python")

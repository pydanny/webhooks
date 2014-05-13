#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_webhooks
----------------------------------

Tests for `webhooks` module.
"""


from webhooks import webhook, unhashed_hook
from webhooks.senders import async_redis
from webhooks.senders import simpleprint
from webhooks.senders import targeted


def test_simpleprint_hashed():

    @webhook(event="example200", sender_callable=simpleprint.sender)
    def basic(wife, husband, creator):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert status['creator'] == "pydanny"
    assert len(status['hash']) > 10


def test_simpleprint_unhash():

    @unhashed_hook(event="example200", sender_callable=simpleprint.sender)
    def basic(wife, husband, creator):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert status['creator'] == "pydanny"
    assert "hash" not in status


def test_targeted_hashed():

    @webhook(sender_callable=targeted.sender)
    def basic(url, wife, husband):
        return {"husband": husband, "wife": wife}

    status = basic(
        url="http://httpbin.org/post",
        husband="Daniel Roy Greenfeld",
        wife="Audrey Roy Greenfeld",
    )

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert len(status['hash']) > 10


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

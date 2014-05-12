#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_webhooks
----------------------------------

Tests for `webhooks` module.
"""


from webhooks import webhook, unhashed_hook
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


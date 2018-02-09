#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_webhooks
----------------------------------

Tests for `webhooks` module.
"""

from webhooks import webhook, unhashed_hook
from webhooks.senders.simple import sender


def test_simple_hashed():

    @webhook(event="example200", sender_callable=sender)
    def basic(wife, husband, creator, encoding):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny", encoding="application/json")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert "creator" not in status
    assert len(status['hash']) > 10


def test_simple_unhash():

    @unhashed_hook(event="example200", sender_callable=sender)
    def basic(wife, husband, creator, encoding):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny", encoding="application/json")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert "hash" not in status

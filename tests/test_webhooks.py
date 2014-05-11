#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_webhooks
----------------------------------

Tests for `webhooks` module.
"""


from webhooks import webhook, unhashed_hook
from webhooks.senders.simpleprint import sender


def test_200():

    @webhook(event="example200", sender_callable=sender)
    def basic(creator="pydanny"):
        return {"name": "Daniel Roy Greenfeld", "spouse": "Audrey Roy Greenfeld"}

    status = basic(creator='pydanny')

    assert status['spouse'] == "Audrey Roy Greenfeld"
    assert status['name'] == "Daniel Roy Greenfeld"
    assert len(status['hash']) > 10


def test_unhooked_hash():

    @unhashed_hook(event="example200", sender_callable=sender)
    def basic(creator="pydanny"):
        return {"name": "Daniel Roy Greenfeld", "spouse": "Audrey Roy Greenfeld"}

    status = basic(creator='pydanny')

    assert status['spouse'] == "Audrey Roy Greenfeld"
    assert status['name'] == "Daniel Roy Greenfeld"
    assert "hash" not in status

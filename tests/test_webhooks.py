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
    def basic(creator="pydanny"):
        return {"husband": "Daniel Roy Greenfeld", "wife": "Audrey Roy Greenfeld"}

    status = basic(creator='pydanny')

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert len(status['hash']) > 10


def test_simpleprint_unhash():

    @unhashed_hook(event="example200", sender_callable=simpleprint.sender)
    def basic(creator="pydanny"):
        return {"husband": "Daniel Roy Greenfeld", "wife": "Audrey Roy Greenfeld"}

    status = basic(creator='pydanny')

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert "hash" not in status


def test_targeted_hashed():

    @webhook(sender_callable=targeted.sender)
    def basic(url):
        return {"husband": "Daniel Roy Greenfeld", "wife": "Audrey Roy Greenfeld"}

    status = basic(url="http://httpbin.org/post")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert len(status['hash']) > 10

    # no argument passed
    status = basic(url="http://httpbin.org/post")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert len(status['hash']) > 10

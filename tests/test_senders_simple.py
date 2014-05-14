#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_webhooks
----------------------------------

Tests for `webhooks` module.
"""

from webhooks import webhook
from webhooks.senders import simple


def test_simpleprint_hashed():

    @webhook(event="example200", sender_callable=simple.sender)
    def basic(wife, husband, creator):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert "creator" not in status
    assert len(status['hash']) > 10

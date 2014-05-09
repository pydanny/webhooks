#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_webhooks
----------------------------------

Tests for `webhooks` module.
"""


from webhooks import webhook
from webhooks.senders.simpleprint import sender


def test_200():

    @webhook(event="example200", sender_callable=sender)
    def basic(creator="pydanny"):
        return {"name": "Daniel Roy Greenfeld", "spouse": "Audrey Roy Greenfeld"}

    basic(creator='pydanny')

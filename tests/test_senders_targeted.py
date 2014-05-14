#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webhooks import webhook
from webhooks.senders import targeted


def test_simple_hashed():
    @webhook(sender_callable=targeted.sender)
    def basic(wife, husband, url):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", url="http://httpbin.org/post")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert len(status['hash']) > 10


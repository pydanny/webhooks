#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_webhooks
----------------------------------

Tests for `webhooks` module.
"""

from webhooks import webhook, unhashed_hook
from webhooks.senders.simple import sender
import json
from standardjson import StandardJSONEncoder
from Crypto.Hash import SHA256


def test_simple_hashed():

    @webhook(event="example200", sender_callable=sender)
    def basic(wife, husband, creator, encoding, url):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny", encoding="application/json", url="http://httpbin.org")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert "creator" not in status
    assert len(status['hash']) > 10


def test_simple_unhash():

    @unhashed_hook(event="example200", sender_callable=sender)
    def basic(wife, husband, creator, encoding, url):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny", encoding="application/json", url="http://httpbin.org")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert "hash" not in status


def test_simple_custom_header():

    @unhashed_hook(event="example200", sender_callable=sender)
    def basic(wife, husband, creator, encoding, url, custom_headers):
        return {"husband": husband, "wife": wife}

    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny", encoding="application/json", custom_headers = {"Basic" : "dXNlcjpzdXBlcnNlY3JldA=="}, url="http://httpbin.org")

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    assert status['post_attributes']['headers']['Basic'] == "dXNlcjpzdXBlcnNlY3JldA=="



def test_simple_signature():

    @unhashed_hook(event="example200", sender_callable=sender)
    def basic(wife, husband, creator, encoding, url, signing_secret):
        return {"husband": husband, "wife": wife}
    secret = "secret_key"
    status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", creator="pydanny", encoding="application/json", url="http://httpbin.org", signing_secret = secret)

    assert status['wife'] == "Audrey Roy Greenfeld"
    assert status['husband'] == "Daniel Roy Greenfeld"
    signature = status['post_attributes']['headers']['x-hub-signature']
    body = {"wife": "Audrey Roy Greenfeld", "husband": "Daniel Roy Greenfeld"}

    if not isinstance(secret, bytes):
        secret = secret.encode('utf-8')
    hash = SHA256.new(secret)
    hash.update(json.dumps(body, cls=StandardJSONEncoder).encode("utf-8"))
    expected_signature = "sha256="+hash.hexdigest()
    assert signature == expected_signature
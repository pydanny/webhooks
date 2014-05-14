#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import Redis


from webhooks import webhook
from webhooks.senders import async_redis


def test_async():

    connection = Redis()  # Connection(Redis())

    # Second, test the sender, which handles the async components
    @webhook(sender_callable=async_redis.sender)
    def sender(url, language, connection):
        return {"language": language, "url": url}

    response = sender(url="http://httpbin.org/post", language="python", connection=connection)
    assert response['status_code'] == 200

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from redis import Redis
from webhooks import webhook
from webhooks.senders import async_redis

class SendersAsyncRedisCase(unittest.TestCase):

    def test_redis_sender(self):

        redis_connection = Redis()

        # Second, test the sender, which handles the async components
        @webhook(sender_callable=async_redis.sender)
        def sender(url, language, connection, encoding):
            return {"language": language, "url": url}

        response = sender(url="http://httpbin.org/post", language="python", connection=redis_connection, encoding='application/json')
        assert response['status_code'] == 200

if __name__ == '__main__':
    unittest.main()

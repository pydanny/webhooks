#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from webhooks import webhook
from webhooks.senders import targeted
import test_base
import json
from ddt import ddt, data

@ddt
class SendersTargetedCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_server = test_base.start_test_server()
        test_base.configure_debug_logging()

    @classmethod
    def tearDownClass(cls):
        test_base.end_test_server(cls.test_server)

    @data("application/x-www-form-urlencoded", "application/json")
    def test_encoding(self, encoding):

        @webhook(sender_callable=targeted.sender)
        def basic(wife, husband, url, encoding):
            return {"husband": husband, "wife": wife}

        status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", url="http://localhost:5000/webhook", encoding=encoding)

        assert status['wife'] == "Audrey Roy Greenfeld"
        assert status['husband'] == "Daniel Roy Greenfeld"
        assert len(status['hash']) > 10

    @data({'timeout': 5, 'expected_success': True}, {'timeout': 0.010, 'expected_success': False})
    def test_timeout(self, params):

        @webhook(sender_callable=targeted.sender)
        def basic(wife, husband, url, encoding, timeout):
            return {"husband": husband, "wife": wife}

        status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", url="http://localhost:5000/webhook", encoding="application/json", timeout=params['timeout'])
        print(status['response'])
        assert (json.loads(status['response'])['status'] == 'success' if params['expected_success'] else json.loads(status['response'])['status'] != 'success')
        assert status['wife'] == "Audrey Roy Greenfeld"
        assert status['husband'] == "Daniel Roy Greenfeld"
        assert len(status['hash']) > 10

if __name__ == '__main__':

    unittest.main()
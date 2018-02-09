#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import unittest
from webhooks import webhook
from webhooks.senders import targeted
from tests import test_base
import json
from ddt import ddt, data

@ddt
class SendersTargetedCase(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        test_base.configure_debug_logging()
        cls.test_server = test_base.start_test_server()

    @classmethod
    def setup_class(cls):
        #test_base.end_test_server(cls.test_server)
        pass

    @data("application/x-www-form-urlencoded", "application/json")
    def test_encoding(self, encoding):

        @webhook(sender_callable=targeted.sender)
        def basic(wife, husband, url, encoding):
            return {"husband": husband, "wife": wife}

        status = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", url="http://localhost:5001/webhook", encoding=encoding)

        assert status['wife'] == "Audrey Roy Greenfeld"
        assert status['husband'] == "Daniel Roy Greenfeld"
        assert len(status['hash']) > 10

    @data({'timeout': 10, 'expected_success': True}, {'timeout': 0.010, 'expected_success': False})
    def test_timeout(self, params):

        @webhook(sender_callable=targeted.sender)
        def basic(wife, husband, url, encoding, timeout):
            return {"husband": husband, "wife": wife}

        response = basic("Audrey Roy Greenfeld", "Daniel Roy Greenfeld", url="http://localhost:5001/webhook", encoding="application/json", timeout=params['timeout'])
        print(response['response'])
        assert (response['success'] if params['expected_success'] else not response['success'])
        assert (not response['error'] if params['expected_success'] else response['error'])
        assert response['wife'] == "Audrey Roy Greenfeld"
        assert response['husband'] == "Daniel Roy Greenfeld"
        assert len(response['hash']) > 10



if __name__ == '__main__':

    unittest.main()
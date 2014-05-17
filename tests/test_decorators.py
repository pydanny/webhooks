#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from webhooks.decorators import cached_property
from webhooks.exceptions import SenderNotCallable
from webhooks import webhook


def test_callable_sender():

    @webhook(event="example200", sender_callable=123)
    def basic(creator="pydanny"):
        return {"husband": "Daniel Roy Greenfeld", "wife": "Audrey Roy Greenfeld"}

    with pytest.raises(SenderNotCallable):
        basic(creator='pydanny')

    def test_cached_property(self):

        class Check(object):

            def __init__(self):
                self.total1 = 0
                self.total2 = 0

            def add_control(self):
                self.total1 += 1
                return self.total1

            @cached_property
            def add_cached(self):
                self.total2 += 1
                return self.total2

        c = Check()

        # The control shows that we can continue to add 1.
        self.assertEqual(c.add_control, 1)
        self.assertEqual(c.add_control, 2)

        # The cached version demonstrates how nothing new is added
        self.assertEqual(c.add_cached, 1)
        self.assertEqual(c.add_cached, 1)

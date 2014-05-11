#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from webhooks.exceptions import SenderNotCallable
from webhooks import webhook, unhashed_hook


def test_callable_sender():

    @webhook(event="example200", sender_callable=123)
    def basic(creator="pydanny"):
        return {"husband": "Daniel Roy Greenfeld", "wife": "Audrey Roy Greenfeld"}

    with pytest.raises(SenderNotCallable):
        basic(creator='pydanny')


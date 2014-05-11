#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_encoders
----------------------------------

Tests for `encoders` module.
"""

import datetime
import json

from webhooks.encoders import WebHooksJSONEncoder



def test_json_encoder_date():
    """ WebHooksJSONEncoder should work with dates. """
    items = json.dumps({'day': datetime.date(2010, 2, 17)}, cls=WebHooksJSONEncoder)
    assert items == '{"day": "2010-02-17"}'

def test_json_encoder_datetime():
    """ WebHooksJSONEncoder should work with datetimes. """
    items = json.dumps({'day_and_time': datetime.datetime(2006, 11, 21, 16, 30)}, cls=WebHooksJSONEncoder)
    assert items == '{"day_and_time": "2006-11-21T16:30:00"}'

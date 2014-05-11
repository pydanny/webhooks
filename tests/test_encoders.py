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

# Unit tests

def test_json_encoder_date():
    """ WebHooksJSONEncoder should work with dates. """
    encoder = WebHooksJSONEncoder()
    items = encoder.default(datetime.date(2010, 2, 17))
    assert items == '2010-02-17'

def test_json_encoder_datetime():
    """ WebHooksJSONEncoder should work with datetimes. """
    encoder = WebHooksJSONEncoder()
    items = encoder.default(datetime.datetime(2006, 11, 21, 16, 30))
    assert items == '2006-11-21T16:30:00'

def test_json_encoder_time():
    """ WebHooksJSONEncoder should work with times. """
    encoder = WebHooksJSONEncoder()
    items = encoder.default(datetime.time(16, 30))
    assert items == '16:30:00'

def test_json_encoder_time_microsecond():
    """ WebHooksJSONEncoder should work with times with microsecond info.
        ECMA-262 says, "sss is the number of complete milliseconds since the 
        start of the second as three decimal digits." """
    encoder = WebHooksJSONEncoder()
    items = encoder.default(datetime.time(16, 30, 01, 123456))
    assert items == '16:30:01.123'

# Integration tests

def test_json_encoder_date_json():
    """ WebHooksJSONEncoder should work with dates. Pass in as dumps() cls parameter. """
    items = json.dumps({'day': datetime.date(2010, 2, 17)}, cls=WebHooksJSONEncoder)
    assert items == '{"day": "2010-02-17"}'

def test_json_encoder_date2_json():
    """ WebHooksJSONEncoder should work with dates. Test via encode()."""
    items = WebHooksJSONEncoder().encode({'day': datetime.date(2010, 2, 17)})
    assert items == '{"day": "2010-02-17"}'

def test_json_encoder_datetime_json():
    """ WebHooksJSONEncoder should work with datetimes. Pass in as dumps() cls parameter. """
    items = json.dumps({'day_and_time': datetime.datetime(2006, 11, 21, 16, 30)}, cls=WebHooksJSONEncoder)
    assert items == '{"day_and_time": "2006-11-21T16:30:00"}'




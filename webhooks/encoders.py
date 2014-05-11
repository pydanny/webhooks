"""
Serialize data to/from JSON
Inspired by https://github.com/django/django/blob/master/django/core/serializers/json.py
"""

# Avoid shadowing the standard library json module
from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import decimal
import json


class WebHooksJSONEncoder(json.JSONEncoder):
    """
    A JSONEncoder that can encode date/time and decimal types.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(WebHooksJSONEncoder, self).default(o)

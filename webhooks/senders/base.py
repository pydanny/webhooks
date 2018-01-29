# -*- coding: utf-8 -*-

from __future__ import absolute_import
import json
import logging
import sys
from time import sleep

from cached_property import cached_property
from standardjson import StandardJSONEncoder
import requests


if not logging.getLogger().getEffectiveLevel():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Senderable(object):

    def __init__(self, wrapped, dkwargs, hash_value, attempts, *args, **kwargs):
        """
            :wrapped: Function that has been wrapped and whose payload is being sent
        """
        self.wrapped = wrapped
        self.dkwargs = dkwargs
        self.hash_value = hash_value
        self.attempts = attempts
        self.args = args
        self.kwargs = kwargs
        self.attempt = 0
        self.success = False
        self.response = None

    @staticmethod
    def _default_timeout():
        return 5

    @cached_property
    def url(self):
        return self.get_url()

    def get_url(self):
        return "http://httpbin.org/post"

    @cached_property
    def encoding(self):
        return self.get_encoding()

    def get_encoding(self):
        encoding = _value_in('encoding', True, kwargs=self.kwargs, dkwargs=self.dkwargs)
        if not encoding or not (encoding == EncodingType.JSON or encoding == EncodingType.FORMS):
            msg = "Invalid choice for 'encoding'. Valid selections are '%s' or '%s'" % (EncodingType.FORMS, EncodingType.JSON)
            raise TypeError(msg)
        return encoding

    @cached_property
    def timeout(self):
        return self.get_timeout()

    def get_timeout(self):
        return _value_in('timeout', False, kwargs=self.kwargs, dkwargs=self.dkwargs) or self._default_timeout()

    @cached_property
    def payload(self):
        return self.get_payload()

    def get_payload(self):
        """
            1. Create the payload by calling the hooked/wrapped function
            2. Add the hash_value if there is one.

        """
        # Create the payload by calling the hooked/wrapped function.
        payload = self.wrapped(*self.args, **self.kwargs)

        # Add the hash value if there is one.
        if self.hash_value is not None and len(self.hash_value) > 0:
            payload['hash'] = self.hash_value

        return payload

    def format_payload(self):
        if self.get_encoding() == EncodingType.JSON:
            return self.jsonify_payload()
        return self.payload

    def jsonify_payload(self):
        """ Dump the payload to JSON """
        return json.dumps(self.payload, cls=StandardJSONEncoder)

    def notify(self, message):
        print(message)
        logging.debug(message)

    def send(self):
        """ Wrapper around _send method for use with asynchronous coding. """
        return self._send()

    def _send(self):
        """ Send the webhook method """

        payload = self.payload
        payload['url'] = self.url

        for i, wait in enumerate(range(len(self.attempts) - 1)):

            self.attempt = i + 1

            payload['attempt'] = self.attempt

            # post the payload
            skip_response = False
            post_attributes = {'timeout' : self.timeout}
            encoding_key = 'json' if self.encoding == EncodingType.JSON else 'data'
            post_attributes[encoding_key] = self.format_payload()
            try:
                self.response = requests.post(self.url, **post_attributes)
            except Exception as ex:
                payload['response'] = '{"status_code": 500, "status":"failure","error":"'+str(ex).replace('"',"'")+'"}'
                skip_response = True

            if not skip_response:
                if sys.version > '3':
                    # Converts bytes object to str object in Python 3+
                    self.response_content = self.response.content.decode('utf-8')
                else:
                    self.response_content = self.response.content

                payload['status_code'] = self.response.status_code

                # anything with a 200 status code  is a success
                if self.response.status_code >= 200 and self.response.status_code < 300:
                    # Exit the sender method.  Here we provide the payload as a result.
                    #   This is useful for reporting.
                    self.success = True
                    self.notify("Attempt {}: Successfully sent webhook {}".format(
                        self.attempt, self.hash_value)
                    )
                    payload['response'] = self.response_content
                    break

            self.notify("Attempt {}: Could not send webhook {}".format(
                    self.attempt, self.hash_value)
            )

            # Wait a bit before the next attempt
            sleep(wait)

        # Exit the send method.  Here we provide the payload as a result.
        return payload

def _value_in(key, required, dkwargs, kwargs):
    if key in kwargs:
        return kwargs[key]
    elif key in dkwargs:
        return dkwargs[key]
    elif required:
        msg = "Sender function needs a %s argument" % key
        raise TypeError(msg)
    return None

def value_in(key, dkwargs, kwargs):
    return _value_in(key, True, dkwargs, kwargs)

def value_in_opt(key, required, dkwargs, kwargs):
    return _value_in(key, required, dkwargs, kwargs)


class EncodingType(object):
    JSON = 'application/x-www-form-urlencoded'
    FORMS = 'application/json'
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import json
import logging
import sys
from time import sleep

from cached_property import cached_property
from standardjson import StandardJSONEncoder
import requests


logging.basicConfig(level=logging.DEBUG)


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

    @cached_property
    def url(self):
        return self.get_url()

    def get_url(self):
        return "http://httpbin.org/post"

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

    @cached_property
    def jsonified_payload(self):
        return self.get_jsonified_payload()

    def get_jsonified_payload(self):
        """ Dump the payload to JSON """
        return json.dumps(self.payload, cls=StandardJSONEncoder)

    def notify(self, message):
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
            self.response = requests.post(self.url, self.payload)
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


def value_in(key, dkwargs, kwargs):
    if key in kwargs:
        return kwargs[key]
    elif key in dkwargs:
        return dkwargs[key]
    else:
        msg = "Sender function needs a %s argument" % key
        raise TypeError(msg)

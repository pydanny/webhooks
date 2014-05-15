# -*- coding: utf-8 -*-

import json
import logging
from time import sleep

import requests

from ..decorators import cached_property
from ..encoders import WebHooksJSONEncoder


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
        return json.dumps(self.payload, cls=WebHooksJSONEncoder)

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

            msg = "Attempt: {attempt}, {url}\n{payload}".format(
                    attempt=self.attempt,
                    url=self.url,
                    payload=self.jsonified_payload
                )
            self.notify(msg)

            payload['attempt'] = self.attempt

            # post the payload
            r = requests.post(self.url, self.payload)
            self.response = r

            payload['status_code'] = r.status_code

            # anything with a 200 status code  is a success
            if r.status_code >= 200 and r.status_code < 300:
                # Exit the sender method.  Here we provide the payload as a result.
                #   This is useful for reporting.
                self.success = True
                self.notify("Successfully sent webhook {}".format(self.hash_value))
                payload['response'] = r.content
                return payload

            # Wait a bit before the next attempt
            sleep(wait)
        else:
            self.success = False
            self.notify("Could not send webhook {}".format(self.hash_value))

        # Exit the send method.  Here we provide the payload as a result for
        #   display when this method is run outside of asynchronous code.
        return payload


def value_in(key, dkwargs, kwargs):
    if key in kwargs:
        return kwargs[key]
    elif key in dkwargs:
        return dkwargs[key]
    else:
        msg = "Sender function needs a %s argument" % key
        raise TypeError(msg)

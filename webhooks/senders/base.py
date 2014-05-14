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

        for attempt in range(len(self.attempts) - 1):
            # Print each attempt. In practice, this would write to logs
            msg = "Attempt: {attempt}, {url}\n{payload}".format(
                    attempt=attempt + 1,
                    url=self.url,
                    payload=self.jsonified_payload
                )
            self.notify(msg)

            # post the payload
            r = requests.post(self.url, self.payload)

            # anything with a 200 status code  is a success
            if r.status_code >= 200 and r.status_code < 300:
                # Exit the sender method.  Here we provide the payload as a result.
                #   This is useful for reporting.
                self.notify("Successfully sent webhook {}".format(self.hash_value))
                return self.payload

            # Wait a bit before the next attempt
            sleep(attempt)
        else:
            self.notify("Could not send webhook {}".format(self.hash_value))

        # Exit the send method.  Here we provide the payload as a result for
        #   display when this method is run outside of asynchronous code.
        return self.payload

# -*- coding: utf-8 -*-

import json
from time import sleep

import requests

from ..encoders import WebHooksJSONEncoder


# First element is 0 to represent the first attempt
ATTEMPTS = [0, 1, 2, 3, 4]


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):
    """
        This is the simplest production-worthy callable I can create. It does 3 things:

            1. calls the hooked/wrapped function and transforms the response
                into JSON.
            2. Uses the url argument as where to send the webhook.
            3. Sends the payload to the target.

        Note: Each line of code written in this function can be expanded on in
        it's own function or method.
    """

    # Get the URL from the kwargs
    url = kwargs.get('url', None)
    if url is None:
        url = dkwargs['url']

    # Create the payload by calling the hooked/wrapped function.
    payload = wrapped(*args, **kwargs)

    # Add the hash value if there is one.
    if hash_value is not None and len(hash_value) > 0:
        payload['hash'] = hash_value

    # Dump the payload to json
    data = json.dumps(payload, cls=WebHooksJSONEncoder)

    # Loop through the attempts and log each attempt
    for attempt in range(len(ATTEMPTS) - 1):

        # Wait a bit before the next attempt
        sleep(attempt)

        # Print each attempt. In practice, this would either write to logs or
        #   submit to a write-fast DB like Redis.
        print(
            "Attempt: {attempt}, {url}\n{payload}".format(
                attempt=attempt + 1,
                url=url,
                payload=data
            )
        )

        # post the payload
        r = requests.post(url, payload)

        # anything with a 200 status code  is a success
        if r.status_code >= 200 and r.status_code < 300:
            # Exit the sender function.  Here we provide the payload as a result.
            #   In practice, this means writing the result to a datastore.
            return payload

        # Log the current status of things and try again.
        # TODO - add logs

    else:
        raise Exception("Could not send webhook")

    # Exit the sender function.  Here we provide the payload as a result.
    #   In practice, this means writing the result to a datastore.
    #   TODO -log
    return payload

# -*- coding: utf-8 -*-

import json
import logging
from time import sleep

import requests
from redis import Redis
import rq
from rq.decorators import job

from ..encoders import WebHooksJSONEncoder


logging.basicConfig(filename="async.log", level=logging.DEBUG)

connection = Redis()
q = rq.Queue(connection=connection)


@job('default', connection=connection, timeout=5)
def worker(wrapped, dkwargs, hash_value=None, *args, **kwargs):

    # First element is 0 to represent the first attempt
    # TODO - pass this in as a decorator argument
    ATTEMPTS = [0, 1, 2, 3, 4]

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

    for attempt in range(len(ATTEMPTS) - 1):
        # Print each attempt. In practice, this would write to logs
        msg = "Attempt: {attempt}, {url}\n{payload}".format(
                attempt=attempt,
                url=url,
                payload=data
            )
        logging.debug(msg)

        # post the payload
        r = requests.post(url, payload)

        # anything with a 200 status code  is a success
        if r.status_code >= 200 and r.status_code < 300:
            # Exit the sender function.  Here we provide the payload as a result.
            #   In practice, this means writing the result to a datastore.
            logging.debug("Success!")
            return payload

        # Log the current status of things and try again.
        # TODO - add logs

        # Wait a bit before the next attempt
        sleep(attempt)
    else:
        logging.debug("Could not send webhook")

    # Exit the sender function.  Here we provide the payload as a result for
    #   display when this function is run outside of the sender function.
    return payload


def sender(wrapped, dkwargs, hash_value=None, *args, **kwargs):

    logging.debug("Starting async")
    worker(wrapped, dkwargs, hash_value=None, *args, **kwargs)
    logging.debug("Ending async")

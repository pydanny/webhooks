# -*- coding: utf-8 -*-

import json
from time import sleep

import requests

from ..encoders import WebHooksJSONEncoder

# This is a simplistic webhooks table. Real lists would probably include the
#   following:
#
#       1. event name (used in lookups)
#       2. creator/owner name of the webhook (used in lookups)
#       3. target url
#       4. content type (optional - JSON, YAML, Form encoding, etc)
#       5. last attempt made (optional)


WEBHOOKS = {
    # event       Target URL
    "example200": "http://httpbin.org/post",
    "example201": "http://httpbin.org/post",
    "example202": "http://httpbin.org/post",
    "example302": "http://httpbin.org/post",
    "example404": "http://httpbin.org/post",
    "example500": "http://httpbin.org/post",

}

# First element is 0 to represent the first attempt
ATTEMPTS = [0, 1, 2, 3, 4]


def sender(wrapped, event, *args, **kwargs):
    """
        This is the simplest sender callable I can create. It does 3 things:

            1. calls the hooked/wrapped function and transforms the response
                into JSON.
            2. Uses the event and creator arguments to find the right webhook.
                A webhook being the target of the send.
            3. Sends the payload to the webhook target.

        For the purposes of designing the API, this is kept as simple as
        possible. However, future sender callables could do the following:

            1. Use Python-based concurrency to allow for threading of the
                actions of this sender function.
            2. Use external queues such as those powered by RabbitMQ, Redis,
                or even SQL databases. Celery and RedisQ should make this
                easy to implement.
            3. If a number of identical payloads to one webhook target are
                generated, they can be combined into one payload.
            4. Be designed specifically for frameworks like Django, SQLAlchemy,
                MongoEngine, et al.
            5. Follow the resthooks patterns more closely.

        Note: Each line of code written in this function can be expanded on in
        it's own function or method.
    """

    # Get the creator. We don't do anything here, but in other sender functions
    #   we would
    creator = kwargs['creator']

    # Create the payload by calling the hooked/wrapped function.
    payload = wrapped(*args, **kwargs)

    # Dump the payload to json
    payload = json.dumps(payload, cls=WebHooksJSONEncoder)

    # Get the target URL using just the event. In practice this would also use
    #   the creator argument as well.
    target_url = WEBHOOKS[event]

    # Loop through the attempts and log each attempt
    for attempt in range(len(ATTEMPTS) - 1):
        # Print each attempt. In practice, this would either write to logs or
        #   submit to a write-fast DB like Redis.
        print(
            "Attempt: {attempt}, {target_url}\n{payload}".format(
                attempt=attempt,
                target_url=target_url,
                payload=payload
            )
        )

        # post the payload
        r = requests.post(target_url, payload)

        # anything with a 200 status code  is a success
        if r.status_code >= 200 and r.status_code < 300:
            # Exit the sender function. We don't provide a return value as the
            #   result of this should be tracked outside the current flow.
            #   In practice, this means writing the result to a datastore.
            print("SUCCESS!!!")
            return payload

        # Print the current status of things and try again.
        #   In practice this would also write a database or logs.
        print(r.status_code)
        print(r.content)

        # Wait a bit before the next attempt
        sleep(attempt)

    # Exit the sender function. We don't provide a return value as the
    #   result of this should be tracked outside the current flow.
    #   In practice, this means writing the result to a datastore.
    print("FAILURE!!!")
    return payload

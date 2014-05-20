# -*- coding: utf-8 -*-

from __future__ import absolute_import
import uuid


def placebo_hash_function():
    return ""


def basic_hash_function():
    return uuid.uuid4().hex

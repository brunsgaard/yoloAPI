#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The core module holds generic functions and the Flask extensions.
"""

from flask.ext.mongoalchemy import MongoAlchemy
from flask_oauthlib.provider import OAuth2Provider
from redis import StrictRedis
from settings import REDIS_URL

db = MongoAlchemy()
oauth = OAuth2Provider()
redis = StrictRedis.from_url(REDIS_URL)

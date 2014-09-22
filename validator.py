#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_oauthlib.provider import OAuth2RequestValidator
from models import User, Client, Token


class MyRequestValidator(OAuth2RequestValidator):
    """ Defines a custom OAuth2 Request Validator based on the Client, User
	and Token models.

	:param OAuth2RequestValidator: Overrides the OAuth2RequestValidator.
	"""
    def __init__(self):
        self._clientgetter = Client.find
        self._usergetter = User.find_with_password
        self._tokengetter = Token.find
        self._tokensetter = Token.save

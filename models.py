#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.mongoalchemy import MongoAlchemy
from datetime import datetime, timedelta
from core import db, redis
import bcrypt

class User(db.Document):
    """ User which will be querying resources from the API.

    :param db.Document: MongoDB document object.
    """

    id       = db.ObjectIdField(required=True)
    username = db.StringField(required=True)
    hashpw   = db.StringField(required=True)

    @staticmethod
    def find_with_password(username, password, *args, **kwargs):
        """ Query the User collection for a record with matching username and
        password hash. If only a username is supplied, find the first matching
        document with that username.

        :param username: Username of the user.
        :param password: Password of the user.
        :param *args: Variable length argument list.
        :param **kwargs: Arbitrary keyword arguments.
        """
        user = User.query.filter_by(username=username).first()
        if user and password:
            encodedpw = password.encode('utf-8')
            userhash  = user.hashpw.encode('utf-8')
            return User.query.filter(User.username == username, User.hashpw == bcrypt.hashpw(encodedpw, userhash)).first()
        else:
            return user

    @staticmethod
    def create(username, password):
        """ Create a new User document with the supplied username and password.

        :param username: Username of the user.
        :param password: Password of the user.
        """
        user_id = db.ObjectIdField().gen()
        salt    = bcrypt.gensalt()
        hash    = bcrypt.hashpw(password.encode('utf-8'), salt)
        user    = User(id=user_id, username=username, hashpw=hash)
        user.save()

    @staticmethod
    def all():
        """ Return all User documents found in the database. """
        return User.query.all()


class Client(db.Document):
    """ Client application through which user is authenticating.

    RFC 6749 Section 2 (http://tools.ietf.org/html/rfc6749#section-2)
    describes clients:

     +----------+
     | Resource |
     |  Owner   |
     |          |
     +----------+
          v
          |    Resource Owner
         (A) Password Credentials
          |
          v
     +---------+                                  +---------------+
     |         |>--(B)---- Resource Owner ------->|               |
     |         |         Password Credentials     | Authorization |
     | Client  |                                  |     Server    |
     |         |<--(C)---- Access Token ---------<|               |
     |         |    (w/ Optional Refresh Token)   |               |
     +---------+                                  +---------------+

    Redirection URIs are mandatory for clients. We skip this requirement
    as this example only allows the resource owner password credentials
    grant (described in Section 4.3). In this flow, the Authorization
    Server will not redirect the user as described in subsection 3.1.2
    (Redirection Endpoint).

    :param db.Document: MongoDB document object.
    """
    client_id   = db.ObjectIdField(required=True)
    client_type = db.StringField(max_length=40, required=True)

    @property
    def allowed_grant_types(self):
        """ Returns allowed grant types.

        Presently, only the password grant type is allowed.
        """
        return ['password']

    @property
    def default_scopes(self):
        """ Returns default scopes associated with the Client. """
        return []

    @staticmethod
    def find(id):
        """ Queries the Client table and returns first client with
            matching id.

        :param id: Client id
        """
        return Client.query.filter_by(client_id=id).first()

    @staticmethod
    def generate():
        """ Generate a new public client with the ObjectID helper."""
        client_id = db.ObjectIdField().gen()
        client    = Client(client_id=client_id, client_type='public')
        client.save()

    @staticmethod
    def all():
        """ Return all Client documents found in the database. """
        return Client.query.all()

    def default_redirect_uri():
        """ Return a blank default redirect URI since we are not implementing
            redirects.
        """
        return ''


class Token(db.Document):
    """ Access or refresh token

        Because of our current grant flow, we are able to associate tokens
        with the users who are requesting them. This can be used to track usage
        and potential abuse. Only bearer tokens currently supported.

        :param db.Document: MongoDB document object.
    """
    client_id     = db.SRefField(Client, required=True)
    client        = client_id.rel()
    user_id       = db.SRefField(User, required=True)
    user          = user_id.rel()
    token_type    = db.StringField(max_length=40)
    access_token  = db.StringField(max_length=40)
    refresh_token = db.StringField(max_length=40)
    expires       = db.DateTimeField()
    scopes        = ['']

    @staticmethod
    def find(access_token=None, refresh_token=None):
        """ Retrieve a token record using submitted access token or 
        refresh token.

        :param access_token: User access token.
        :param refresh_token: User refresh token.
        """
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()

    @staticmethod
    def delete(self):
        """ Delete token from MongoDB and Redis cache. """
        self.remove()
        redis.delete(self.access_token)
        return self

    @staticmethod
    def stash(token, request, *args, **kwargs):
        """ Save a new token to the MongoDB token collection.

        The stash function also manipulates tokens in the local Redis cache, so the API can
        validate if a token is acceptable without needing to know anything about a user's
        credentials.

        :param token: Token dictionary containing access and refresh tokens, plus token type.
        :param request: Request dictionary containing information about the client and user.
        :param *args: Variable length argument list.
        :param **kwargs: Arbitrary keyword arguments.  
        """
        toks = Token.query.filter_by(client_id=request.client.client_id, user_id=request.user.id)

        # Ensure each client has only one token connected per user.
        for t in toks:
            t.remove()
            redis.delete(t.access_token)

        expires_in = token.pop('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        tok = Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user.id
        )

        # Add the access token to the Redis cache and set it to
        # expire at the appropriate time.
        user = User.query.filter_by(id=request.user.id).first()
        tokenuser = user.username
        redis.setex(token['access_token'], expires_in, tokenuser)

        tok.save()

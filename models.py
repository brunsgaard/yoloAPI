from datetime import datetime, timedelta
from werkzeug.security import gen_salt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User which owns resources behind our own api"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))

    @staticmethod
    def find_with_password(username, password, *args, **kwargs):
        if password:
            return User.query.filter_by(
                username=username, password=password).first()
        else:
            return User.query.filter_by(username=username).first()

    @staticmethod
    def save(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def all():
        return User.query.all()


class Client(db.Model):
    """http://tools.ietf.org/html/rfc6749#section-2

    RFC 6749 Section 2 describes clients.

    One thing to note is that redirection URIs are mandatory for clients. We
    skip this requrement as this example will only allow the resource owner
    password credentials grant(described in section 4.3).

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

    In this flow the Authorization Server will not redirect the user as
    described in subsection 3.1.2 (Redirection Endpoint).

    """

    client_id = db.Column(db.String(40), primary_key=True)
    client_type = db.Column(db.String(40))

    @property
    def allowed_grant_types(self):
        return ['password']

    @property
    def default_scopes(self):
        return []

    @staticmethod
    def find(id):
        return Client.query.filter_by(client_id=id).first()

    @staticmethod
    def generate():
        client = Client(client_id=gen_salt(40), client_type='public')
        db.session.add(client)
        db.session.commit()

    @staticmethod
    def all():
        return Client.query.all()

    def default_redirect_uri():
        return ''


class Token(db.Model):
    """Access or refresh token

    Note that an access token is aware about to which user and client it was
    issued, thus we can identify which user is making a request based on this
    token.
    """

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'),
                          nullable=False)
    client = db.relationship('Client')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)

    @staticmethod
    def find(access_token=None, refresh_token=None):
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()

    @staticmethod
    def save(token, request, *args, **kwargs):
        toks = Token.query.filter_by(
            client_id=request.client.client_id,
            user_id=request.user.id
        )
        # make sure that every client has only one token connected to a user
        for t in toks:
            db.session.delete(t)

        expires_in = token.pop('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        tok = Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user.id,
        )
        db.session.add(tok)
        db.session.commit()

from app import db


class User(db.Model):
    """User which owns resources behind our own api"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))


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

    id = db.Column(db.String(40), primary_key=True)
    type = db.Column(db.String(40))


class Token(db.Model):
    """Token that allows access to the API

    Note that an access token is aware about to which user and client it was
    issued, thus we can identify which user is making a request based on this
    token.
    """

    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)

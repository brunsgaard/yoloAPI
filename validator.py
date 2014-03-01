from flask_oauthlib.provider import OAuth2Provider, OAuth2RequestValidator
from models import User, Client, Token

oauth = OAuth2Provider()

class MyRequestValidator(OAuth2RequestValidator):

    _clientgetter = Client.find

    _usergetter = User.find

    _tokengetter = Token.find
    _tokensetter = Token.save

    _grantgetter = lambda *args, **kwargs: None
    _grantsetter = lambda *args, **kwargs: None

    def __init__(self):
        pass


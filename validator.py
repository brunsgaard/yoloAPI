from flask_oauthlib.provider import OAuth2Provider, OAuth2RequestValidator
from models import User, Client, Token
import logging

log = logging.getLogger('flask_oauthlib')

oauth = OAuth2Provider()

class MyRequestValidator(OAuth2RequestValidator):


    def __init__(self):
        self._clientgetter = Client.find

        self._usergetter = User.find_with_password

        self._tokengetter = Token.find
        self._tokensetter = Token.save

        self._grantgetter = lambda *args, **kwargs: None
        self._grantsetter = lambda *args, **kwargs: None

    def client_authentication_required(self, request, *args, **kwargs):
        return False




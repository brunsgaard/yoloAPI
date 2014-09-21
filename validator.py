from flask_oauthlib.provider import OAuth2RequestValidator
from models import User, Client, Token

class MyRequestValidator(OAuth2RequestValidator):
    """
    Explain what this can be used for.
    """

    def __init__(self):
        self._clientgetter = Client.find
        self._usergetter = User.find_with_password
        self._tokengetter = Token.find
        self._tokensetter = Token.save

from flask_oauthlib.provider import OAuth2RequestValidator
from models import User, Client, Token


class MyRequestValidator(OAuth2RequestValidator):
    """
    To understand the reason purpose of this class read
    http://flask-oauthlib.readthedocs.org/en/latest/api.html#flask_oauthlib.provider.OAuth2RequestValidator
    """

    def __init__(self):
        self._clientgetter = Client.find
        self._usergetter = User.find_with_password
        self._tokengetter = Token.find
        self._tokensetter = Token.save

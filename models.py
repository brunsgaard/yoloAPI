
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Client(db.Model):

    client_id = db.Column(db.String(40), primary_key=True)
    client_type_ = db.Column(db.Enum(('public', 'confidentail')))
    _allow_grant_types = db.Column( )

    @property
    def client_secret():
        return None

    @property
    def default_redirect_uri():
        return None

    @property
    def default_scopes():
        return []

    @property
    def allowed_grant_types():
        if _allow_grant_types:
            return _allow_grant_types.split()
        return []

    def validate_scopes(self, client_id, scopes, client, request,
                        *args, **kwargs):
        return True


class Token(db.Model):
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
    _scopes = db.Column(db.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

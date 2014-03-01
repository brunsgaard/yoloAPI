from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from models import User, Client, db
from flask import request
from flask_oauthlib.provider import OAuth2Provider
from validator import oauth, MyRequestValidator

app = Flask(__name__)
app.debug = True
app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sqlite',
})
db.init_app(app)
oauth.init_app(app)
oauth._validator = MyRequestValidator()


@app.route('/', methods=['GET', 'POST'])
def management():
    if request.method == 'POST' and request.form['submit'] == 'adduser':
        User.save(request.form['username'],request.form['password'])
    if request.method == 'POST' and request.form['submit'] == 'addclient':
        Client.generate()
    return render_template('management.html', users=User.all(), clients=Client.all())


@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token(*args, **kwargs):
    return None

import logging
logger = logging.getLogger('flask_oauthlib')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    db.create_all(app=app)
    app.run()

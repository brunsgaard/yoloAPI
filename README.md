# Yolo API

This is a Flask-OAuthlib server example for the 'Resource Owner Password Credentials Grant' described in [RFC 6749 (Section 1.3.3)](http://tools.ietf.org/html/rfc6749#section-1.3.3).

## Deployment

Clone this repository and install all dependencies:

```bash
$ pip install -r requirements.txt
```

Once all dependencies are installed, you may run the application using `python app.py`.

## User and Client Management

For the example to work properly, you will need to create a client and user. You can create users and clients through the management interface available at [http://localhost:5000](http://localhost:5000).

## Testing

After creating a user and client, you may use curl to test the application.

### Generating a Bearer Token

```bash
$ curl -X POST -d "client_id=9qFbZD4udTzFVYo0u5UzkZX9iuzbdcJDRAquTfRk&grant_type=password&username=jonas&password=pass" http://localhost:5000/oauth/token
{"access_token": "NYODXSR8KalTPnWUib47t5E8Pi8mo4", "token_type": "Bearer", "refresh_token": "s6L6OPL2bnKSRSbgQM3g0wbFkJB4ML", "scope": ""}
```

### Accessing a Protected Resource Using Retrieved Bearer Token

```bash
$ curl -H "Authorization: Bearer NYODXSR8KalTPnWUib47t5E8Pi8mo4" http://localhost:5000/yolo
YOLO! Congraulations, you made it through and accessed the protected resource!
```

## Security
This example uses bcrypt and a randomly generated salt to hash each user password before it is added to the database. You should never store passwords in plain text!


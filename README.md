yoloAPI
===================================================================
An flask-oauthlib server example for 'Resource Owner Password Credentials Grant'

##### Get it up and running
To get it up and running clone this repository and install the dependencies.
```bash
pip install -r requirements.txt
```
After this you can run the application with `python app.py`.

##### Management
At this point you should to go `http://localhost:5000` and generate a client and also create a user.
Now you can use `curl` for testing the application and the access the protected resource.

##### Get a Bearer token

```bash
curl -X POST -d "client_id=9qFbZD4udTzFVYo0u5UzkZX9iuzbdcJDRAquTfRk&grant_type=password&username=jonas&password=pass" http://localhost:5000/oauth/token
{"access_token": "NYODXSR8KalTPnWUib47t5E8Pi8mo4", "token_type": "Bearer", "refresh_token": "s6L6OPL2bnKSRSbgQM3g0wbFkJB4ML", "scope": ""}
```

##### Use the Bearer token to access the protected resource
```bash
curl -H "Authorization: Bearer NYODXSR8KalTPnWUib47t5E8Pi8mo4" http://localhost:5000/yolo
YOLO!!! You made it through and accessed the protected resource
```

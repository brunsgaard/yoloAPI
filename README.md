flask-oauthlib-server-example-ResourceOwnerPasswordCredentialsGrant
===================================================================

Example for OAuth 2 Server (Resource Owner Password Credentials)

curl -X POST -d "client_id=9qFbZD4udTzFVYo0u5UzkZX9iuzbdcJDRAquTfRk&grant_type=password&username=jonas&password=pass" http://localhost:5000/oauth/token

{"access_token": "NYODXSR8KalTPnWUib47t5E8Pi8mo4", "token_type": "Bearer", "refresh_token": "s6L6OPL2bnKSRSbgQM3g0wbFkJB4ML", "scope": ""}

curl -H "Authorization: Bearer ubI7o3REXb943CUtnZ14c6mLVHJrby" http://localhost:5000/yolo

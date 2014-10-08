#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The application server
APPLICATION_SERVER = 'localhost'

# The port which this service should listen on.
APPLICATION_PORT = 5100

# Application debug setting.
DEBUG = True

# The MongoDB server.
# Default: 'localhost'
MONGOALCHEMY_SERVER = 'localhost'

# Listening port of the MongoDB server.
# Default: 27017
MONGOALCHEMY_PORT = 27017

# The database name that should be used for the connection.
# Default: N/A
MONGOALCHEMY_DATABASE = 'accounts'

# Boolean value indicating to use server based authentication 
# or not. When False, will use database based authentication.
# Default: True
MONGOALCHEMY_SERVER_AUTH = False

# User for database connection.
# Default: None
MONGOALCHEMY_USER = None

# Password for database connection.
# Default: None
MONGOALCHEMY_PASSWORD = None

# Use session in safe mode. When in safe mode, all methods 
# like save and delete wait for the operation to complete.
# Default: False
MONGOALCHEMY_SAFE_SESSION = False

# Pass extra options to the MongoDB server when connecting.
# Default: None
MONGOALCHEMY_OPTIONS = None

# The Redis URL path.
# Format redis://username:password@server:port/db
REDIS_URL = 'redis://localhost:6379/0'

# Indicate whether or not management screen is active.
# Ultimately, this should be active for specific IPs, etc. only.
MANAGEMENT_ENABLED = True
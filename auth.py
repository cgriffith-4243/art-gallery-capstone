import json
import os
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

## AuthError Exception
'''
AuthError Exception
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'authorization header expected'
        }, 401)

    header_parts = auth_header.split(' ')  
    if len(header_parts) <= 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'token not found'
        }, 401)
    elif len(header_parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'invalid header format'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'authorization header must be Bearer token'
        }, 401)

    return header_parts[1]

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'permissions not in JWT'
        }, 401)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'permission not found'
        }, 401)
    return True

'''
    @INPUTS
        token: a json web token (string)

    NOTE! Source for this implementation found here: https://auth0.com/docs/quickstart/backend/python/01-authorization
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'authorization malformed'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'token expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'incorrect claims, check audience and issuer'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'unable to parse authentication token'
            }, 401)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'unable to find the appropriate key'
    }, 401)




'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

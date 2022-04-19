import os
import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_ALGORITHMS = os.environ['AUTH0_ALGORITHMS'].split(',')
AUTH0_API_AUDIENCE = os.environ['AUTH0_API_AUDIENCE']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
HOST = os.environ['HOST']


def get_login_url():
	url = f'https://{AUTH0_DOMAIN}/authorize?'
	param = {
		'audience': AUTH0_API_AUDIENCE,
		'response_type': 'token',
		'client_id': AUTH0_CLIENT_ID,
		'redirect_uri': HOST + '/login_callback',
	}

	for k, v in param.items():
		url += k + '=' + v + '&'

	return url[:-1]


def get_logout_url():
	url = f'https://{AUTH0_DOMAIN}/v2/logout?'
	param = {
		'client_id': AUTH0_CLIENT_ID,
		'returnTo': HOST + '/logout_callback',
	}

	for k, v in param.items():
		url += k + '=' + v + '&'

	return url[:-1]


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        raise AuthError({
            'code': 'header_missing',
            'description': 'Authorization header missing.'
        }, 401)
    
    header_parts = auth_header.split(' ')
    if len(header_parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid header.'
        }, 401)

    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'bad_token',
            'description': 'The token must start with bearer.'
        }, 401)
    
    if header_parts[1] == '' or header_parts[1] == 'null':
        raise AuthError({
            'code': 'bad_token',
            'description': 'The token content is empty.'
        }, 401)

    return header_parts[1]


def check_permissions(needed_permission, payload):
    if needed_permission != '':
        user_permissions = payload.get('permissions', [])
        if len(user_permissions) == 0:
            raise AuthError({
                'code': 'invalid_permission',
                'description': 'The permission is mission.',
            }, 403)
        
        if needed_permission not in user_permissions:
            raise AuthError({
                'code': 'action_forbidden',
                'description': 'The action of user is forbidden.',
            }, 403)


def verify_decode_jwt(token):
    jwks_request = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jwks_request.read())
    unverified_header = jwt.get_unverified_header(token)
    
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.',
        }, 401)

    rsa_key = None
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token = token,
                key = rsa_key,
                algorithms = AUTH0_ALGORITHMS,
                audience = AUTH0_API_AUDIENCE,
                issuer = f'https://{AUTH0_DOMAIN}/',
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.',
            }, 401)
        
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)

    else:
        raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)
        

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
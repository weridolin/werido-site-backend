import jwt

def generate_jwt_token(payload, secret_key, algorithm='HS256'):
    return jwt.encode(payload, secret_key, algorithm=algorithm)

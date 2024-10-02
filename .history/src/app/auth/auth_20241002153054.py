import jwt
import datetime
import os

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

def decode_jwt(token):
    
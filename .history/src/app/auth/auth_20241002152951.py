import jwt
import datetime
import os

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": 
    }
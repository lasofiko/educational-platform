from fastapi import Header
from fastapi.exceptions import HTTPException
import jwt, os


def get_current_user(authorization: str = Header(default=None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Wrong JWT format")

    token = authorization.removeprefix("Bearer ")

    try:
        payload = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])
    except jwt.PyJWTError as e:
        raise HTTPException(401, "Incorrect JWT")

    return payload
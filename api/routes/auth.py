from typing import Optional
from fastapi import APIRouter, Header

import jwt

router = APIRouter()

@router.get("/user/roles", name="auth:getUserRoles")
def user_roles(authorization: Optional[str] = Header(None)):
    try:
        encoded_token = authorization.split(" ")[1]
        pub_key = "keycloakPublicKey"
        client_id = "someString"
        algorithm = ["RS256"]
        decoded_token = jwt.decode(encoded_token, pub_key, client_id, algorithm)

        user = {
          "name": decoded_token["name"],
          "username": decoded_token["preferred_username"],
          "email": decoded_token["email"],
          "cac": decoded_token["activecac"],
          "groups": decoded_token["group-simple"]
        }
    except AttributeError:
        return None

    return user

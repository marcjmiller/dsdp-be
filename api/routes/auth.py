from typing import Optional
from fastapi import APIRouter, Header

import jwt

router = APIRouter()

@router.get("/user/roles", name="auth:getUserRoles")
def user_roles(authorization: Optional[str] = Header(None)):
    try:
        encoded_token = authorization.split(" ")[1]
        pk = "keycloakPublicKey"
        audience = "someString" # whatever the name of the client used for the app is, ex: "il19_00eb8094-2f88-4c98-ad87-dsdp"
        decoded_token = jwt.decode(encoded_token, pk, audience, algorithms=["RS256"])

        user = {
          "name": decoded_token["name"],
          "username": decoded_token["preferred_username"],
          "email": decoded_token["email"],
          "cac": decoded_token["activecac"],
          "groups": decoded_token["group-simple"]
        }
    except:
        return None

    return user

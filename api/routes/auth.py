from typing import Optional
from fastapi import APIRouter, Header
from jwt import DecodeError

import jwt
import requests

router = APIRouter()


@router.get("/user/roles", name="auth:getUserRoles")
def user_roles(authorization: Optional[str] = Header(None)):
    pub_key = ""
    client_id = ""
    try:
        encoded_token = authorization.split(" ")[1]
        print("Got encoded token")
        baby_yoda = requests.get("https://login.dso.mil/auth/realms/baby-yoda/").json()
        print("got baby yoda info")
        pub_key = f"-----BEGIN PUBLIC KEY-----\n{baby_yoda['public_key']}\n-----END PUBLIC KEY-----"
        print("got pub key")
        client_id = "il2_00eb8904-5b88-4c68-ad67-cec0d2e07aa6_mission-staging"
        algorithm = ["RS256"]
        print("about to try decoding")
        decoded_token = jwt.decode(encoded_token, pub_key, client_id, algorithm)

        print("attempting to create user")
        user = {
            "name": decoded_token["name"],
            "username": decoded_token["preferred_username"],
            "email": decoded_token["email"],
            "cac": decoded_token["activecac"],
            "groups": decoded_token["group-simple"],
        }
    except AttributeError:
        print(f"Attribute error, Auth: {authorization}")
        return {"Message": "Attribute Error, see container logs"}
    except KeyError:
        print(f"Key error, \nPubKey: {pub_key} \nAuth: {authorization}")
        return {"Message:": "Invalid KEYCLOAK_PUBLIC_KEY, see container logs"}
    except DecodeError:
        print(
            f"Decode error, Auth: {authorization}, Key {pub_key}, Audience: {client_id}"
        )
        return {"Message": "Decode Error, see container logs"}
    except Exception as exception:
        print(
            f"Auth:{authorization}, Key: {pub_key}, Client ID: {client_id}, Except: {exception}"
        )
        raise exception
    return user

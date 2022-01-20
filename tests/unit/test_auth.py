import pytest
import requests
from api.routes.auth import user_roles
from mock import MagicMock

def test_auth(mocker):
    return_value={
        "name": "user name",
        "preferred_username": "user.name",
        "email": "useremail",
        "activecac": "",
        "group-full": ["Products-Teams/Dsdp", "/Product-Teams/Dsdp/Admin"],
    }
    expected_user_obj = {
        "name": "user name",
        "username": "user.name",
        "email": "useremail",
        "cac": "",
        "groups": ["Products-Teams/Dsdp", "/Product-Teams/Dsdp/Admin"],
        "isAdmin": True
    }
    mock = mocker.patch("api.routes.auth.decode", MagicMock())
    mock.return_value = return_value
    baby_yoda = requests.get("https://login.dso.mil/auth/realms/baby-yoda/").json()
    pub_key = f"-----BEGIN PUBLIC KEY-----\n{baby_yoda['public_key']}\n-----END PUBLIC KEY-----"
    user_obj = user_roles("bearer fakebearertoken")
    mock.assert_called_with('fakebearertoken', options={'verify_signature': False})
    assert user_obj==expected_user_obj
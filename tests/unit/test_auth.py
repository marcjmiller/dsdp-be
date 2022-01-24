from api.routes.auth import who_am_i
from mock import MagicMock
from api.models.user_info import UserInfo

JWT_STUB = {
    "name": "user name",
    "preferred_username": "user.name",
    "email": "useremail",
    "activecac": "",
    "group-full": ["Products-Teams/Dsdp", "/Product-Teams/Dsdp/Admin", "/Platform One/gvsc/IL2/roles/admin"],
}


def test_auth(mocker):
    expected_user_obj = UserInfo(name="user name", is_admin=True)
    mock = mocker.patch("api.routes.auth.decode", MagicMock())
    mock.return_value = JWT_STUB

    user_obj = who_am_i("bearer fakebearertoken")

    mock.assert_called_with("fakebearertoken", options={"verify_signature": False})
    assert user_obj == expected_user_obj

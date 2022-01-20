import pytest
from api.routes.auth import user_roles
from mock import MagicMock

def test_auth(mocker):
    mock = mocker.patch("backend.api.routes.auth.jwt.decode", MagicMock())
    user_roles()
    mock.assert_called_with("", "", "", "")
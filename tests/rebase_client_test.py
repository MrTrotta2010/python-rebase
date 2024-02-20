# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import pytest

from src.python_rebase.rebase_client import ReBaseClient

class TestReBaseClient:
    def test_init(self):
        client = ReBaseClient('test@gmail.com', 'authtoken')

        assert client.user_email == 'test@gmail.com'
        assert client.user_token == 'authtoken'

    def test_init_errors(self):
        with pytest.raises(TypeError):
            ReBaseClient('wrong number of arguments') # pylint: disable=no-value-for-parameter

        with pytest.raises(ValueError):
            ReBaseClient(None, 'authtoken')
        with pytest.raises(ValueError):
            ReBaseClient(12, 'authtoken')
        with pytest.raises(ValueError):
            ReBaseClient('email', None)
        with pytest.raises(ValueError):
            ReBaseClient('email', 12)

# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import pytest

from src.python_rebase import util
from src.python_rebase.session import Session
from src.python_rebase.movement import Movement

class TestUtil:
    def test_is_valid_str(self):
        assert util.is_valid_str('a')
        assert util.is_valid_str('')
        assert not util.is_valid_str(1)
        assert not util.is_valid_str(None)
        assert not util.is_valid_str(True)
        assert not util.is_valid_str(False)

    def test_is_valid_number(self):
        assert util.is_valid_number(1)
        assert util.is_valid_number(-1)
        assert util.is_valid_number(0)
        assert util.is_valid_number(2.4)
        assert not util.is_valid_number('')
        assert not util.is_valid_number(None)
        assert not util.is_valid_number(True)
        assert not util.is_valid_number(False)

    def test_is_valid_id(self):
        assert util.is_valid_id(1)
        assert util.is_valid_id('1')
        assert not util.is_valid_id(-1)
        assert not util.is_valid_id(0)
        assert not util.is_valid_id(2.4)
        assert not util.is_valid_id('')
        assert not util.is_valid_id(None)
        assert not util.is_valid_id(True)
        assert not util.is_valid_id(False)

    def test_is_valid_movement_field(self):
        assert util.is_valid_movement_field('id', 1)
        assert not util.is_valid_movement_field('ide', 1)
        assert not util.is_valid_movement_field('title', 'oi!')

    def test_is_valid_session_field(self):
        assert util.is_valid_session_field('id', 1)
        assert not util.is_valid_session_field('ide', 1)
        assert util.is_valid_session_field('title', 'oi!')

    def test_exclude_keys_from_dict(self):
        dictionary = { 'a': 1, 'b': 2, 'c': 3 }
        util.exclude_keys_from_dict(dictionary, ['a', 'b'])
        assert dictionary == { 'c': 3 }

    def test_validate_initialization_dict(self):
        with pytest.raises(ValueError):
            Movement({ 'invalid': { 'object': 'value' }})

        with pytest.raises(ValueError):
            Session({ 'invalid': { 'object': 'value' }})

# pylint: enable=missing-module-docstring, missing-class-docstring, missing-function-docstring

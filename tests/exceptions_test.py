# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import pytest

from src.pyrebase.missing_attribute_error import MissingAttributeError
from src.pyrebase.mismatched_articulations_error import MismatchedArticulationsError
from src.pyrebase.repeated_articulation_error import RepeatedArticulationError

class TestExceptions:
    def test_exceptions(self):
        with pytest.raises(MissingAttributeError):
            raise MissingAttributeError('attribute')

        with pytest.raises(MismatchedArticulationsError):
            raise MismatchedArticulationsError(['a1'], ['a2'])

        with pytest.raises(RepeatedArticulationError):
            raise RepeatedArticulationError('a1', ['a1', 'a1'])

    def test_messages(self):
        missing_e = MissingAttributeError('attribute')
        mismatched_e = MismatchedArticulationsError(['a1'], ['a2'])
        repeated_e = RepeatedArticulationError('a1', ['a1', 'a1'])

        assert str(missing_e) == "Essential attribute 'attribute' is missing from request"
        assert str(mismatched_e) == "Articulation lists do not match: ['a1'] and ['a2']"
        assert str(repeated_e) == "Duplicate articulation 'a1' in list ['a1', 'a1']"

# pylint: enable=missing-module-docstring, missing-class-docstring, missing-function-docstring

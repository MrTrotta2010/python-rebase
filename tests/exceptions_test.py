import pytest

from src.pyrebase.missing_attribute_error import MissingAttributeError
from src.pyrebase.mismatched_articulations_error import MismatchedArticulationsError
from src.pyrebase.repeated_articulation_error import RepeatedArticulationError

class TestExceptions:
  def test_missing_attribute_error(self):
    with pytest.raises(MissingAttributeError):
      raise MissingAttributeError('attribute')

  def test_missing_attribute_error_message(self):
    e = MissingAttributeError('attribute')
    assert str(e) == "Essential attribute 'attribute' is missing from request"

  def test_mismatched_articulation_error(self):
    with pytest.raises(MismatchedArticulationsError):
      raise MismatchedArticulationsError(['a1'], ['a2'])

  def test_mismatched_articulation_error_message(self):
    e = MismatchedArticulationsError(['a1'], ['a2'])
    assert str(e) == "Articulation lists do not match: ['a1'] and ['a2']"

  def test_repeated_articulation_error(self):
    with pytest.raises(RepeatedArticulationError):
      raise RepeatedArticulationError('a1', ['a1', 'a1'])

  def test_repeated_articulation_error_message(self):
    e = RepeatedArticulationError('a1', ['a1', 'a1'])
    assert str(e) == "Duplicate articulation 'a1' in list ['a1', 'a1']"

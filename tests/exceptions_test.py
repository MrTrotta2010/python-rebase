import pytest

from src.pyrebase.missing_attribute_exception import MissingAttributeException
from src.pyrebase.mismatched_articulations_exception import MismatchedArticulationsException
from src.pyrebase.repeated_articulation_exception import RepeatedArticulationException

class TestExceptions:
  def test_missing_attribute_exception(self):
    with pytest.raises(MissingAttributeException):
      raise MissingAttributeException('attribute')

  def test_missing_attribute_exception_message(self):
    e = MissingAttributeException('attribute')
    assert str(e) == "Essential attribute 'attribute' is missing from request"

  def test_mismatched_articulations_exception(self):
    with pytest.raises(MismatchedArticulationsException):
      raise MismatchedArticulationsException(['a1'], ['a2'])

  def test_mismatched_articulations_exception_message(self):
    e = MismatchedArticulationsException(['a1'], ['a2'])
    assert str(e) == "Articulation lists do not match: ['a1'] and ['a2']"

  def test_repeated_articulation_exception(self):
    with pytest.raises(RepeatedArticulationException):
      raise RepeatedArticulationException('a1', ['a1', 'a1'])

  def test_repeated_articulation_exception_message(self):
    e = RepeatedArticulationException('a1', ['a1', 'a1'])
    assert str(e) == "Duplicate articulation 'a1' in list ['a1', 'a1']"

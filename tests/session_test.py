import pytest

from src.pyrebase.session import Session
from src.pyrebase.movement import Movement
from src.pyrebase.register import Register
from src.pyrebase.mismatched_articulations_error import MismatchedArticulationsError

class TestSession:
  def test_init(self):
    session = Session({ 'title': 'Test', 'id': 0 })

    assert session.title == 'Test'
    assert session.id == 0

  def test_init_with_movement(self):
    movements = [
      Movement({ 'articulations': ['a1'], 'articulationData': [{ 'a1': [1, 2, 3] }], 'duration': 10 }),
      Movement({ 'articulations': ['a1'], 'articulationData': [{ 'a1': [1, 2, 3] }], 'duration': 10 })
    ]
    session = Session({ 'title': 'Test', 'id': 0, 'movements': movements })

    assert len(session.movements) == 2
    assert session.duration == movements[0].duration + movements[1].duration

  def test_conversions(self):
    original_dict = { 'id': '0', 'title': 'test', 'patientId': 'foo', 'movements': [Movement({ 'label': 'move' })] }
    expected_str = "{'id': '0', 'title': 'test', 'patient': {'id': 'foo'}, 'movements': [{'label': 'move'}]}"
    expected_json = "{\"title\": \"test\", \"patient\": {\"id\": \"foo\"}, \"movements\": [{\"label\": \"move\"}]}"
    expected_update_json = "{\"title\": \"test\", \"patient\": {\"id\": \"foo\"}}"
    session = Session(original_dict)

    session_dict = session.to_dict()

    assert session_dict['id'] == original_dict['id']
    assert session_dict['title'] == original_dict['title']
    assert session_dict['patient']['id'] == original_dict['patientId']
    assert isinstance(session_dict['movements'], list)
    assert isinstance(session_dict['movements'][0], dict)
    assert session_dict['movements'][0]['label'] == 'move'

    assert str(session) == expected_str
    assert session.to_json(update=False) == expected_json
    assert session.to_json(update=True) == expected_update_json

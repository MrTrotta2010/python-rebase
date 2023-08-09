import pytest

from src.pyrebase.movement import Movement
from src.pyrebase.register import Register
from src.pyrebase.mismatched_articulations_error import MismatchedArticulationsError

class TestMovement:
  def test_init(self):
    movement = Movement({ 'label': 'test', 'device': 'py' })

    assert movement.label == 'test'
    assert movement.device == 'py'

  def test_init_with_data(self):
    with pytest.raises(MismatchedArticulationsError):
      movement = Movement({ 'articulationData': [{ 'a1': [1, 2, 3] }] })

    movement = Movement({ 'articulations': ['a1'], 'articulationData': [{ 'a1': [1, 2, 3] }] })

    assert len(movement.articulation_data) == 1
    assert movement.articulation_data[0] == Register({ 'a1': [1, 2, 3] })

  def test_articulation_data(self):
    movement_a = Movement({ 'articulations': ['a1', 'a2'] })
    movement_a.articulation_data = [{ 'a1': [1, 2, 3], 'a2': [4, 5, 6] }]
    movement_b = Movement({ 'articulations': ['a1', 'a2'] })
    movement_b.articulation_data = [Register({ 'a1': [1, 2, 3], 'a2': [4, 5, 6] })]
    movement_c = Movement()
    movement_c.articulation_data = { 'a1': [1, 2, 3], 'a2': [4, 5, 6] }

    assert len(movement_a.articulation_data) == len(movement_b.articulation_data)
    assert movement_a.articulation_data[0] == movement_b.articulation_data[0]
    assert movement_c.articulation_data == []
    assert movement_a.number_of_registers == movement_b.number_of_registers == 1

  def test_add_register(self):
    empty_movement = Movement()
    diff_movement = Movement({ 'articulations': ['a20'] })
    movement = Movement({ 'articulations': ['a1'] })

    empty_movement.add_register({ 'a1': [1, 2, 3] })
    movement.add_register(Register({ 'a1': [1, 2, 3] }))
    movement.add_register({ 'a1': [4, 5, 6] })

    with pytest.raises(MismatchedArticulationsError):
      diff_movement.add_register({ 'a1': [1, 2, 3] })

    assert empty_movement.articulations == ['a1']
    assert len(movement.articulation_data) == 2
    assert movement.articulation_data[1] == Register({ 'a1': [4, 5, 6] })

  def test_conversions(self):
    original_dict = { 'label': 'test', 'fps': 30, 'articulations': ['a1'], 'articulationData': [Register({ 'a1': [1, 2, 3] })] }
    expected_str = "{'label': 'test', 'articulations': ['a1'], 'fps': 30, 'duration': 0.03333333333333333, 'numberOfRegisters': 1, 'articulationData': {'a1': [[1, 2, 3]]}}"
    expected_json = "{\"label\": \"test\", \"fps\": 30, \"duration\": 0.03333333333333333, \"numberOfRegisters\": 1, \"articulationData\": {\"a1\": [[1, 2, 3]]}}"
    expected_update_json = "{\"label\": \"test\", \"fps\": 30}"
    movement = Movement(original_dict)

    movement_dict = movement.to_dict()
    original_dict['duration'] = None
    original_dict['numberOfRegisters'] = None

    print(movement.to_json(True))

    assert movement_dict.keys() == original_dict.keys()
    assert movement_dict['label'] == original_dict['label']
    assert movement_dict['fps'] == original_dict['fps']
    assert movement_dict['articulations'] == original_dict['articulations']
    assert isinstance(movement_dict['articulationData'], dict)
    assert isinstance(movement_dict['articulationData']['a1'], list)
    assert movement_dict['articulationData']['a1'][0] == [1, 2, 3]

    assert str(movement) == expected_str
    assert movement.to_json(update=False) == expected_json
    assert movement.to_json(update=True) == expected_update_json

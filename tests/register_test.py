import pytest

from src.pyrebase.register import Register
from src.pyrebase.rotation import Rotation
from src.pyrebase.repeated_articulation_exception import RepeatedArticulationException

class TestRegister:
  def test_init(self):
    register_n = Register()
    register_l = Register(['a1'])
    register_d = Register({ 'a1': None, 'a2': None })

    assert register_n.articulations() == []
    assert register_l.articulations() == ['a1']
    assert register_d.articulations() == ['a1', 'a2']
  
  def test_force_rotation(self):
    register = Register({ 'a1': [1, 2, 3], 'a2': Rotation(1, 2, 3) })
    assert register.articulations() == ['a1', 'a2']
    assert isinstance(register['a1'], Rotation)
    assert register['a1'] == register['a2']
  
  def test_force_rotation_invalid_parameters(self):
    with pytest.raises(TypeError):
      Register({ 'a1': 12 })

    with pytest.raises(TypeError):
      Register(14)

    with pytest.raises(RepeatedArticulationException):
      Register(['a1', 'a1'])

  def test_setitem(self):
    register1 = Register()
    register2 = Register()
    register1['a1'] = [1, 2, 3]
    register2['a1'] = Rotation(1, 2, 3)

    assert register1['a1'] == Rotation(1, 2, 3)
    assert register2['a1'] == Rotation(1, 2, 3)

  def test_getitem(self):
    register = Register({ 'a1': Rotation(1, 2, 3) })
    assert register['a1'] == Rotation(1, 2, 3)

  def test_props(self):
    register = Register(['a1', 'a2', 'a3'])
    empty_register = Register()

    assert register.articulation_count() == 3
    assert register.articulations() == ['a1', 'a2', 'a3']
    assert register.is_empty() == False
    assert empty_register.is_empty() == True

  def test_str(self):
    register = Register(['a1', 'a2'])
    assert str(register) == '{a1: [0, 0, 0], a2: [0, 0, 0]}'

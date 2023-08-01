import pytest
from src.pyrebase.rotation import Rotation

class TestRotation:
  def test_init(self):
    rotation = Rotation(1, 2, 3)
    rotation2 = Rotation(1, 2)

    assert rotation.x == 1
    assert rotation.y == 2
    assert rotation.z == 3

    assert rotation2.x == 1
    assert rotation2.y == 2
    assert rotation2.z is None

  def test_str(self):
    rotation = Rotation(1, 2, 3)
    rotation2 = Rotation(1, 2.5)

    assert str(rotation) == '[1, 2, 3]'
    assert str(rotation2) == '[1, 2.5]'
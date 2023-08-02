class Rotation:
  def __init__(self, x: int | float = None, y: int | float = None, z: int | float = None):
    self.x = x or 0
    self.y = y or 0
    self.z = z or 0

  def __eq__(self, other):
    return isinstance(other, Rotation) and self.x == other.x and self.y == other.y and self.z == other.z

  def __str__(self):
    return f'[{round(self.x, 4)}, {round(self.y, 4)}, {round(self.z, 4)}]'

class Rotation:
  def __init__(self, x, y, z = None):
    self.x = x
    self.y = y
    self.z = z

  def __str__(self):
    return f'[{self.x}, {self.y}{("" if self.z is None else f", {self.z}")}]'

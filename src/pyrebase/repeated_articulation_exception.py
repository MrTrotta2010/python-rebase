class RepeatedArticulationException(Exception):
  def __init__(self, art, art_list, *args):
    super().__init__(args)
    self.art = art
    self.art_list = art_list

  def __str__(self):
    return f'Duplicate articulation \'{self.art}\' in list {self.art_list}'

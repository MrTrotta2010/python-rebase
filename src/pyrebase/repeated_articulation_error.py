"""Module that provides the RepeatedArticulationError class"""

class RepeatedArticulationError(Exception):
    """Error thrown when an articulation list has repeated articulations"""

    def __init__(self, art: str, art_list: list, *args):
        super().__init__(args)
        self.art = art
        self.art_list = art_list

    def __str__(self):
        return f'Duplicate articulation \'{self.art}\' in list {self.art_list}'

"""Module that provides the MismatchedArticulationsError class"""

class MismatchedArticulationsError(Exception):
    """Error thrown when two articulation lists do not match"""
    def __init__(self, list_1: list, list_2: list, *args):
        super().__init__(args)
        self.list_1 = list_1
        self.list_2 = list_2

    def __str__(self):
        return f'Articulation lists do not match: {self.list_1} and {self.list_2}'

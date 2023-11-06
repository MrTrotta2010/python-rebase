"""Module that provides the MissingAttributeError class"""

class MissingAttributeError(Exception):
    """Error thrown when an essential attribute is missing from a request"""

    def __init__(self, attribute: str, *args):
        super().__init__(args)
        self.attribute = attribute

    def __str__(self):
        return f'Essential attribute \'{self.attribute}\' is missing from request'

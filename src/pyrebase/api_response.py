"""This module contains the APIResponse class, which represents a response from the server"""
from enum import Enum
from .movement import Movement
from .session import Session

class APIResponse:
    """Represents a response from the ReBase Server"""

    class ResponseType(Enum):
        """Enumerator for the different types of API responses"""
        FETCH_MOVEMENTS = 0
        FIND_MOVEMENT = 1
        INSERT_MOVEMENT = 3
        UPDATE_MOVEMENT = 4
        DELETE_MOVEMENT = 5
        FETCH_SESSIONS = 6
        FIND_SESSION = 7
        INSERT_SESSION = 8
        UPDATE_SESSION = 9
        DELETE_SESSION = 10
        API_ERROR = 11

    def __init__(self, response_type: ResponseType = None, status: int = 0, code: int = 200,
                    data: dict = None, meta: dict = None): # pylint: disable=too-many-arguments
        self.response_type = response_type
        self.status = status
        self.code = code
        self._data = data or {}
        self._meta = meta or {}
        self.__ensure_objects()

    def __str__(self):
        return f'APIResponse: {{ type: {self.human_response_type}, status: {self.status}, ' + \
            f'code: {self.code},\n\tdata: {{ {self.__str_data()} }},\n\tmeta: {self._meta}\n}}'

    def success(self) -> bool:
        """Returns true if the response was successful, false otherwise"""
        return self.status == 0

    def get_data(self, key: str = None):
        """Returns the data associated with the given key, or None if the key is not found"""
        if key is None:
            return None
        return self._data.get(key)

    def has_data(self, key: str = None) -> bool:
        """Returns true if the response has data associated with the given key, false otherwise"""
        return key in self._data

    def get_meta_data(self, key: str = None):
        """Returns the meta data associated with the given key, or None if the key is not found"""
        if key is None:
            return None
        return self._meta.get(key)

    def has_meta_data(self, key: str = None) -> bool:
        """Returns true if the response has meta data associated with the given key, false otherwise"""
        return key in self._meta

    def __get_human_response_type(self):
        # pylint: disable=too-many-return-statements

        if self.response_type == APIResponse.ResponseType.FETCH_MOVEMENTS:
            return 'Fetch Movements'
        if self.response_type == APIResponse.ResponseType.FIND_MOVEMENT:
            return 'Find Movement'
        if self.response_type == APIResponse.ResponseType.INSERT_MOVEMENT:
            return 'Insert Movement'
        if self.response_type == APIResponse.ResponseType.UPDATE_MOVEMENT:
            return 'Update Movement'
        if self.response_type == APIResponse.ResponseType.DELETE_MOVEMENT:
            return 'Delete Movement'
        if self.response_type == APIResponse.ResponseType.FETCH_SESSIONS:
            return 'Fetch Sessions'
        if self.response_type == APIResponse.ResponseType.FIND_SESSION:
            return 'Find Session'
        if self.response_type == APIResponse.ResponseType.INSERT_SESSION:
            return 'Insert Session'
        if self.response_type == APIResponse.ResponseType.UPDATE_SESSION:
            return 'Update Session'
        if self.response_type == APIResponse.ResponseType.DELETE_SESSION:
            return 'Delete Session'
        return 'API Error'

    human_response_type = property(__get_human_response_type)

    def __ensure_objects(self):
        if self.has_data('movement'):
            self._data['movement'] = Movement(self._data['movement'])
        if self.has_data('movements'):
            self._data['movements'] = [Movement(movement) for movement in self._data['movements']]
        if self.has_data('session'):
            self._data['session'] = Session(self._data['session'])
        if self.has_data('sessions'):
            self._data['sessions'] = [Session(movement) for movement in self._data['sessions']]

    def __str_data(self):
        return { k: str(self._data[k]) for k in self._data }

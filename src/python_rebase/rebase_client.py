"""Module that provides methods for send requests to the ReBase Server"""

# Copyright © 2023-2024 Tiago Trotta

# This file is part of Python ReBase.

# Python ReBase is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Python ReBase is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Python ReBase.  If not, see <https://www.gnu.org/licenses/>

from enum import Enum
import requests

from .missing_attribute_error import MissingAttributeError
from .api_response import APIResponse
from .movement import Movement
from .session import Session

_SERVER_URL = "http://projetorastreamento.com.br:3030/"

class _Resource(Enum):
    MOVEMENT = 0
    SESSION = 1

class _Method(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3

class ReBaseClient:
    """Class that provides methods for sending requests to the ReBaseRS"""

    def __init__(self, user_email: str, user_token: str):
        if user_email is None or not isinstance(user_email, str):
            raise ValueError('user_email must be provided and be a string')
        if user_token is None or not isinstance(user_token, str):
            raise ValueError('user_token must be provided and be a string')

        self.user_email = user_email
        self.user_token = user_token

    def __get_headers(self):
        return { 'rebase-user-email': self.user_email, 'rebase-user-token': self.user_token }

    authentication_headers = property(fget=__get_headers, doc='The authentication headers used in the requests')

    def fetch_movements(self, professional_id: str = '', patient_id: str = '', movement_label: str = '', articulations: list = None, legacy: bool = False, page: int = 0, per: int = 0, previous_id: str = '') -> APIResponse:
        """Gets a list of Movements. Can be filtered by professional_id, patient_id, movement_label
        and articulations. Supports pagination. Use the legacy parameter to retrieve the Movements
        in the old ReBase format"""

        return self.__send_request(_Method.GET, _Resource.MOVEMENT, APIResponse.ResponseType.FETCH_MOVEMENTS, params=self.__format_params(professionalId=professional_id, patientId=patient_id, movementLabel=movement_label, articulations=articulations, page=page, per=per, previousId=previous_id, legacy=legacy))

    def find_movement(self, movement_id: str, legacy: bool = False) -> APIResponse:
        """Finds a specific Movement by ID"""

        if (movement_id is None or movement_id == ''):
            raise MissingAttributeError('movement id')

        return self.__send_request(_Method.GET, _Resource.MOVEMENT, APIResponse.ResponseType.FIND_MOVEMENT, movement_id, self.__format_params(legacy=legacy))

    def insert_movement(self, movement: Movement) -> APIResponse:
        """Creates a new Movement"""

        return self.__send_request(_Method.POST, _Resource.MOVEMENT, APIResponse.ResponseType.INSERT_MOVEMENT, data=movement.to_json())

    def update_movement(self, movement: Movement) -> APIResponse:
        """Updates an existing Movement"""

        if (movement.id is None or movement.id == ''):
            raise MissingAttributeError('movement id')

        return self.__send_request(_Method.PUT, _Resource.MOVEMENT, APIResponse.ResponseType.UPDATE_MOVEMENT, movement.id, data=movement.to_json(True))

    def delete_movement(self, movement_id: str) -> APIResponse:
        """Deletes a Movement by ID"""

        if (movement_id is None or movement_id == ''):
            raise MissingAttributeError('movement id')

        return self.__send_request(_Method.DELETE, _Resource.MOVEMENT, APIResponse.ResponseType.DELETE_MOVEMENT, movement_id)

    def fetch_sessions(self, professional_id: str = "", patient_id: str = "", movement_label: str = "", articulations: list = None, legacy: bool = False, page: int = 0, per: int = 0, previous_id: str = '') -> APIResponse:
        """Gets a list of Sessions. Can be filtered by professional_id and patient_id.
        The Sessions' Movements can be filtered by movement_label and articulations.
        Supports pagination. Use the legacy parameter to retrieve the Sessions
        in the old ReBase format"""

        return self.__send_request(_Method.GET, _Resource.SESSION, APIResponse.ResponseType.FETCH_SESSIONS, params=self.__format_params(professionalId=professional_id, patientId=patient_id, movementLabel=movement_label, articulations=articulations, page=page, per=per, previousId=previous_id, legacy=legacy))

    def find_session(self, session_id: str, legacy: bool = False) -> APIResponse:
        """Finds a specific Session by ID"""

        if (session_id is None or session_id == ''):
            raise MissingAttributeError('session id')

        return self.__send_request(_Method.GET, _Resource.SESSION, APIResponse.ResponseType.FIND_SESSION, session_id, self.__format_params(legacy=legacy))

    def insert_session(self, session: Session) -> APIResponse:
        """Creates a new Session"""

        return self.__send_request(_Method.POST, _Resource.SESSION, APIResponse.ResponseType.INSERT_SESSION, data=session.to_json())

    def update_session(self, session: Session) -> APIResponse:
        """Updates an existing Session"""

        if (session.id is None or session.id == ''):
            raise MissingAttributeError('session id')

        return self.__send_request(_Method.PUT, _Resource.SESSION, APIResponse.ResponseType.UPDATE_SESSION, session.id, data=session.to_json(True))

    def delete_session(self, session_id: str, deep: bool = False) -> APIResponse:
        """Deletes a Session by ID"""

        if (session_id is None or session_id == ''):
            raise MissingAttributeError('session id')

        return self.__send_request(_Method.DELETE, _Resource.SESSION, APIResponse.ResponseType.DELETE_SESSION, session_id, self.__format_params(deep=deep))

    def __send_request(self, method: _Method, resource: _Resource, response_type: APIResponse.ResponseType, resource_id: str = None, params: dict = None, data: dict = None) -> APIResponse:
        url = _SERVER_URL + ('movement' if resource == _Resource.MOVEMENT else 'session')
        if resource_id is not None:
            url += f'/{resource_id}'

        try:
            if method == _Method.GET:
                response = requests.get(url, headers=self.authentication_headers, params=params, timeout=30)
            elif method == _Method.POST:
                response = requests.post(url, headers={ 'Content-Type': 'application/json', **self.authentication_headers }, params=params, data=data, timeout=30)
            elif method == _Method.PUT:
                response = requests.put(url, headers={ 'Content-Type': 'application/json', **self.authentication_headers }, params=params, data=data, timeout=30)
            elif method == _Method.DELETE:
                response = requests.delete(url, headers=self.authentication_headers, params=params, timeout=30)
        except requests.exceptions.RequestException as e:
            return self.__new_api_error_response(str(e))

        return self.__parse_api_response(response, response_type)

    def __parse_api_response(self, response: requests.Response, response_type: APIResponse.ResponseType) -> APIResponse:
        if response.status_code < 200 or response.status_code > 300:
            return self.__new_api_response(APIResponse.ResponseType.API_ERROR, response.json(), response.status_code, 1)

        return self.__new_api_response(response_type, response.json(), response.status_code, 0)

    def __new_api_response(self, response_type: APIResponse.ResponseType, response: str, response_code: int, response_status: int) -> APIResponse:
        if response is None:
            return self.__new_api_error_response(response)

        data = response
        meta = data.get('meta')
        del data['status']
        if meta is not None:
            del data['meta']

        return APIResponse(response_type=response_type, status=response_status, code=response_code, data=data, meta=meta)


    def __new_api_error_response(self, response: str) -> APIResponse:
        return APIResponse(response_type=APIResponse.ResponseType.API_ERROR, data={ 'HTMLError': response })

    def __format_params(self, **kwargs) -> dict:
        return { k: v for k, v in kwargs.items() if v is not None and v != '' and v != [] and v != {} and v != 0 }

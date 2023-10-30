import requests

from .missing_attribute_error import MissingAttributeError
from .api_response import APIResponse
from .movement import Movement
from .session import Session
from enum import Enum

_SERVER_URL = "http://projetorastreamento.com.br:3030/"

class __Resource(Enum):
	MOVEMENT = 0
	SESSION = 1

class __Method(Enum):
	GET = 0
	POST = 1
	PUT = 2
	DELETE = 3

def fetch_movements(professional_id: str = '', patient_id: str = '', movement_label: str = '', articulations: list = None, legacy: bool = False, page: int = 0, per: int = 0, previous_id: str = '') -> APIResponse:
	return __send_request(__Method.GET, __Resource.MOVEMENT, APIResponse.ResponseType.FETCH_MOVEMENTS, params=__format_params(professionalId=professional_id, patientId=patient_id, movementLabel=movement_label, articulations=articulations, page=page, per=per, previousId=previous_id, legacy=legacy))

def find_movement(id: str, legacy: bool = False) -> APIResponse:
	if (id is None or id == ''): raise MissingAttributeError('movement id');

	return __send_request(__Method.GET, __Resource.MOVEMENT, APIResponse.ResponseType.FIND_MOVEMENT, id, __format_params(legacy=legacy))

def insert_movement(movement: Movement) -> APIResponse:
	return __send_request(__Method.POST, __Resource.MOVEMENT, APIResponse.ResponseType.INSERT_MOVEMENT, data=movement.to_json())

def update_movement(movement: Movement) -> APIResponse:
	if (movement.id is None or movement.id == ''): raise MissingAttributeError('movement id')

	return __send_request(__Method.PUT, __Resource.MOVEMENT, APIResponse.ResponseType.UPDATE_MOVEMENT, movement.id, data=movement.to_json(True))

def delete_movement(id: str) -> APIResponse:
	if (id is None or id == ''): raise MissingAttributeError('movement id')

	return __send_request(__Method.DELETE, __Resource.MOVEMENT, APIResponse.ResponseType.DELETE_MOVEMENT, id)

def fetch_sessions(professional_id: str = "", patient_id: str = "", movement_label: str = "", articulations: list = None, legacy: bool = False, page: int = 0, per: int = 0, previous_id: str = '') -> APIResponse:
	return __send_request(__Method.GET, __Resource.SESSION, APIResponse.ResponseType.FETCH_SESSIONS, params=__format_params(professionalId=professional_id, patientId=patient_id, movementLabel=movement_label, articulations=articulations, page=page, per=per, previousId=previous_id, legacy=legacy))

def find_session(id: str, legacy: bool = False) -> APIResponse:
	if (id is None or id == ''): raise MissingAttributeError('session id')

	return __send_request(__Method.GET, __Resource.SESSION, APIResponse.ResponseType.FIND_SESSION, id, __format_params(legacy=legacy))

def insert_session(session: Session) -> APIResponse:
	return __send_request(__Method.POST, __Resource.SESSION, APIResponse.ResponseType.INSERT_SESSION, data=session.to_json())

def update_session(session: Session) -> APIResponse:
	if (session.id is None or session.id == ''): raise MissingAttributeError('session id')

	return __send_request(__Method.PUT, __Resource.SESSION, APIResponse.ResponseType.UPDATE_SESSION, session.id, data=session.to_json(True))

def delete_session(id: str, deep: bool = False) -> APIResponse:
	if (id is None or id == ''): raise MissingAttributeError('session id')

	return __send_request(__Method.DELETE, __Resource.SESSION, APIResponse.ResponseType.DELETE_SESSION, id, __format_params(deep=deep))

def __send_request(method: __Method, resource: __Resource, response_type: APIResponse.ResponseType, resource_id: str = None, params: dict = {}, data: dict = {}) -> APIResponse:
	url = _SERVER_URL + ('movement' if resource == __Resource.MOVEMENT else 'session')
	if resource_id != None: url += f'/{resource_id}'

	try:
		if method == __Method.GET:
			response = requests.get(url, params=params)
		elif method == __Method.POST:
			response = requests.post(url, headers={ 'Content-Type': 'application/json' }, params=params, data=data)
		elif method == __Method.PUT:
			response = requests.put(url, headers={ 'Content-Type': 'application/json' }, params=params, data=data)
		elif method == __Method.DELETE:
			response = requests.delete(url, params=params)
	except requests.exceptions.RequestException as e:
		return __new_api_error_response(e.Message)

	return __parse_api_response(response, response_type)

def __parse_api_response(response: requests.Response, response_type: APIResponse.ResponseType) -> APIResponse:
	if response.status_code < 200 or response.status_code > 300:
		return __new_api_response(APIResponse.ResponseType.API_ERROR, response.json(), response.status_code, 1)

	return __new_api_response(response_type, response.json(), response.status_code, 0)

def __new_api_response(response_type: APIResponse.ResponseType, response: str, response_code: int, response_status: int) -> APIResponse:
	try:
		if response is None: return __new_api_error_response(response)
		data = response
		meta = data.get('meta')
		del data['status']
		if meta is not None: del data['meta']
		return APIResponse(response_type=response_type, status=response_status, code=response_code, data=data, meta=meta)

	except Exception as e:
		return __new_api_error_response(str(e))

def __new_api_error_response(response: str) -> APIResponse:
	return APIResponse(response_type=APIResponse.ResponseType.API_ERROR, data={ 'HTMLError': response })

def __format_params(**kwargs) -> dict:
	return { k: v for k, v in kwargs.items() if v is not None and v != '' and v != [] and v != {} and v != 0 }

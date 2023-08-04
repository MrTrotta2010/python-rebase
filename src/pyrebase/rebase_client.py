import requests

from .missing_attribute_error import MissingAttributeError
from .api_response import APIResponse
from .movement import Movement
from .session import Session
from enum import Enum

class ReBaseClient:
	_SERVER_URL = "http://projetorastreamento.com.br:3030/"

	class __Resource(Enum):
		MOVEMENT = 0
		SESSION = 1

	class __Method(Enum):
		GET = 0
		POST = 1
		PUT = 2
		DELETE = 3

	_instance = None

	@classmethod
	def instance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	def fetch_movements(self, professional_id: str = '', patient_id: str = '', movement_label: str = '', articulations: list = None, legacy: bool = False, page: int = 0, per: int = 0, previous_id: str = '') -> APIResponse:
		return self.__send_request(self.__Method.GET, self.__Resource.MOVEMENT, APIResponse.ResponseType.FETCH_MOVEMENTS, params=self.__format_params(professionalId=professional_id, patientId=patient_id, movementLabel=movement_label, articulations=articulations, page=page, per=per, previousId=previous_id, legacy=legacy))

	def find_movement(self, id: str, legacy: bool = False) -> APIResponse:
		if (id is None or id == ''): raise MissingAttributeError('movement id');

		return self.__send_request(self.__Method.GET, self.__Resource.MOVEMENT, APIResponse.ResponseType.FIND_MOVEMENT, id, self.__format_params(legacy=legacy))

	def insert_movement(self, movement: Movement) -> APIResponse:
		return self.__send_request(self.__Method.POST, self.__Resource.MOVEMENT, APIResponse.ResponseType.INSERT_MOVEMENT, data=movement.ToJson())

	def update_movement(self, id: str, movement: Movement) -> APIResponse:
		if (id is None or id == ''): raise MissingAttributeError('movement id')

		return self.__send_request(self.__Method.PUT, self.__Resource.MOVEMENT, APIResponse.ResponseType.UPDATE_MOVEMENT, id, data=movement.ToJson(True))

	def update_movement(self, movement: Movement) -> APIResponse:
		if (movement.id is None or movement.id == ''): raise MissingAttributeError('movement id')

		return self.__send_request(self.__Method.PUT, self.__Resource.MOVEMENT, APIResponse.ResponseType.UPDATE_MOVEMENT, movement.id, data=movement.ToJson(True))

	def delete_movement(self, id: str) -> APIResponse:
		if (id is None or id == ''): raise MissingAttributeError('movement id')

		return self.__send_request(self.__Method.DELETE, self.__Resource.MOVEMENT, APIResponse.ResponseType.DELETE_MOVEMENT, id)

	def fetch_sessions(self, professional_id: str = "", patient_id: str = "", movement_label: str = "", articulations: list = None, legacy: bool = False, page: int = 0, per: int = 0, previous_id: str = '') -> APIResponse:
		return self.__send_request(self.__Method.GET, self.__Resource.SESSION, APIResponse.ResponseType.FETCH_SESSIONS, params=self.__format_params(professionalId=professional_id, patientId=patient_id, movementLabel=movement_label, articulations=articulations, page=page, per=per, previousId=previous_id, legacy=legacy))

	def find_session(self, id: str, legacy: bool = False) -> APIResponse:
		if (id is None or id == ''): raise MissingAttributeError('session id')

		return self.__send_request(self.__Method.GET, self.__Resource.SESSION, APIResponse.ResponseType.FIND_SESSION, id, self.__format_params(legacy=legacy))

	def insert_session(self, session: Session) -> APIResponse:
		return self.__send_request(self.__Method.POST, self.__Resource.SESSION, APIResponse.ResponseType.INSERT_SESSION, data=session.ToJson())

	def update_session(self, session: Session) -> APIResponse:
		if (session.id is None or session.id == ''): raise MissingAttributeError('session id')

		return self.__send_request(self.__Method.PUT, self.__Resource.SESSION, APIResponse.ResponseType.UPDATE_SESSION, session.id, data=session.ToJson(True))

	def delete_session(self, id: str, deep: bool = False) -> APIResponse:
		if (id is None or id == ''): raise MissingAttributeError('session id')

		return self.__send_request(self.__Method.DELETE, self.__Resource.SESSION, APIResponse.ResponseType.DELETE_SESSION, id, self.__format_params(deep=deep))

	def __send_request(self, method: __Method, resource: __Resource, response_type: APIResponse.ResponseType, resource_id: str = None, params: dict = {}, data: dict = {}) -> APIResponse:
		url = self._SERVER_URL + ('movement' if resource == self.__Resource.MOVEMENT else 'session')
		if resource_id != None: url += f'/{resource_id}'

		try:
			if method == self.__Method.GET:
				response = requests.get(url, params=params)
			elif method == self.__Method.POST:
				response = requests.post(url, params=params, data=data)
			elif method == self.__Method.PUT:
				response = requests.put(url, params=params, data=data)
			elif method == self.__Method.DELETE:
				response = requests.delete(url, params=params)
		except requests.exceptions.RequestException as e:
			return self.__new_api_error_response(e.Message)

		return self.__parse_api_response(response, response_type)

	def __parse_api_response(self, response: requests.Response, response_type: APIResponse.ResponseType) -> APIResponse:
		if response.status_code < 200 or response.status_code > 300:
			return self.__new_api_response(APIResponse.ResponseType.API_ERROR, response.json(), response.status_code, 1)

		return self.__new_api_response(response_type, response.json(), response.status_code, 0)

	def __new_api_response(self, response_type: APIResponse.ResponseType, response: str, response_code: int, response_status: int) -> APIResponse:
		print('new_api_response')
		try:
			if response is None: return self.__new_api_error_response(response)
			data = response
			meta = data['meta']
			del data['status']
			del data['meta']
			return APIResponse(response_type=response_type, status=response_status, code=response_code, data=data, meta=meta)

		except Exception as e:
			return self.__new_api_error_response(str(e))

	def __new_api_error_response(self, response: str) -> APIResponse:
		response_object = APIResponse(response_type=APIResponse.ResponseType.API_ERROR)
		response_object.data['HTMLError'] = response
		return response_object;

	def __format_params(self, **kwargs) -> dict:
		return { k: v for k, v in kwargs.items() if v is not None and v != '' and v != [] and v != {} and v != 0 }

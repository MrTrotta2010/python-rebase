from enum import Enum

class APIResponse:
	class ResponseType(Enum):
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

	def __init__(self, response_type: ResponseType = None, status: int = 0, code: int = 200, data: dict = {}, meta: dict = {}):
		self.response_type = response_type
		self.status = status
		self.code = code
		self.data = data
		self.meta = meta

	def __str__(self):
		return f'APIResponse: {{ type: {self.response_type}, status: {self.status}, code: {self.code},\n\tdata: {self.data},\n\tmeta: {self.meta}\n}}'

	def success(self) -> bool:
		return self.status == 0

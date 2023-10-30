from .rotation import Rotation
from .repeated_articulation_error import RepeatedArticulationError


class Register:
	def __init__(self, articulations: list | dict = None):
		self._articulations = {}
		self.__set_articulations(articulations)

	def __setitem__(self, articulation: str, rotation: Rotation | list) -> None:
		self._articulations[articulation] = self.__force_rotation(rotation)

	def __getitem__(self, articulation: str) -> Rotation:
		return self._articulations[articulation]

	def __eq__(self, other) -> bool:
		if not isinstance(other, Register): return False
		if self.articulations != other.articulations: return False

		for art in self.articulations:
			if self[art] != other[art]: return False

		return True

	def __str__(self) -> str:
		return str(self.to_dict())
	
	def to_dict(self) -> dict:
		return { art: value.to_array() for art, value in self._articulations.items() }

	def __get_articulation_count(self) -> int:
		return len(self._articulations)

	def __get_articulations(self) -> list:
		return list(self._articulations.keys())

	def __get_is_empty(self) -> bool:
		return len(self._articulations) == 0

	articulation_count = property(__get_articulation_count)
	articulations = property(__get_articulations)
	is_empty = property(__get_is_empty)

	# Define quais articulações estarão no dicionário
	def __set_articulations(self, articulations: list | dict = None) -> None:
		if articulations is None: return

		if isinstance(articulations, dict):
			for art, value in articulations.items():
				self._articulations[art] = self.__force_rotation(value)

		elif isinstance(articulations, list):
			for articulation in articulations:
				if articulation not in self._articulations:
					self._articulations[articulation] = Rotation()
				else:
					raise RepeatedArticulationError(articulation, articulations)
		
		else:
			raise TypeError(f'Invalid articulation parameter (expected dictionary or list): {articulations}')

	def __force_rotation(self, obj: Rotation | list) -> Rotation:
		if obj is None: return None
		if isinstance(obj, Rotation): return obj
		if isinstance(obj, list): return Rotation(obj[0], obj[1], obj[2])
		raise TypeError(f'Invalid object to be used as rotation (expected Rotation or list): {obj}')

from .rotation import Rotation
from .repeated_articulation_exception import RepeatedArticulationException


class Register:
	def __init__(self, articulations: list | dict = None):
		self._articulations = {}
		self.__set_articulations(articulations)

	def __setitem__(self, articulation: str, rotation: Rotation | list) -> None:
		self._articulations[articulation] = self.__force_rotation(rotation)

	def __getitem__(self, articulation: str) -> Rotation:
		return self._articulations[articulation]

	def __str__(self) -> str:
		string = '{'

		for art, value in self._articulations.items():
			string += f'{art}: {str(value)}, '

		return string[:-2] + '}'
	
	def articulation_count(self) -> int:
		return len(self._articulations)

	def articulations(self) -> list:
		return list(self._articulations.keys())

	def is_empty(self) -> bool:
		return len(self._articulations) == 0

	# Define quais articulações estarão no dicionário
	def __set_articulations(self, articulations: list | dict = None) -> None:
		if articulations is None: return

		if isinstance(articulations, dict):
			print(articulations)
			for art, value in articulations.items():
				print(art, value)
				self._articulations[art] = self.__force_rotation(value)

		elif isinstance(articulations, list):
			for articulation in articulations:
				if articulation not in self._articulations:
					self._articulations[articulation] = Rotation()
				else:
					raise RepeatedArticulationException(articulation, articulations)
		
		else:
			raise TypeError(f'Invalid articulation parameter (expected dictionary or list): {articulations}')

	def __force_rotation(self, obj: Rotation | list) -> Rotation:
		print(obj)
		if obj is None: return None
		if isinstance(obj, Rotation): return obj
		if isinstance(obj, list): return Rotation(obj[0], obj[1], obj[2])
		raise TypeError(f'Invalid object to be used as rotation (expected Rotation or list): {obj}')

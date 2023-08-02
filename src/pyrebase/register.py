from .rotation import Rotation

class Register:
	# private Dictionary<string, Rotation> _articulations;

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
			for art, value in articulations.items():
				self._articulations[art] = self.__force_rotation(value)

		elif isinstance(articulations, list):
			for articulation in articulations:
				if articulation not in self._articulations:
					self._articulations[articulation] = Rotation()
				else:
					# throw new RepeatedArticulationException("Duplicate articulation in list", articulationList);
					pass

	def __force_rotation(self, obj: Rotation | list) -> Rotation:
		if isinstance(obj, Rotation): return obj
		elif isinstance(obj, list): return Rotation(obj[0], obj[1], obj[2])
		else:
			# throw new InvalidTypeException("Invalid type for rotation", object);
			pass

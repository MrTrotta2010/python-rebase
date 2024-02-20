"""Module that provides the Register class"""

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

from .rotation import Rotation
from .repeated_articulation_error import RepeatedArticulationError

class Register:
    """Represents a ReBase Register"""

    def __init__(self, articulations: list | dict = None):
        self._articulations = {}
        self.__set_articulations(articulations)

    def __setitem__(self, articulation: str, rotation: Rotation | list) -> None:
        self._articulations[articulation] = self.__force_rotation(rotation)

    def __getitem__(self, articulation: str) -> Rotation:
        return self._articulations[articulation]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Register):
            return False
        if self.articulations != other.articulations:
            return False

        for art in self.articulations:
            if self[art] != other[art]:
                return False

        return True

    def __str__(self) -> str:
        return str(self.to_dict())

    def to_dict(self) -> dict:
        """Converts the Register to a dictionary"""

        return { art: value.to_list() for art, value in self._articulations.items() }

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
        if articulations is None:
            return

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

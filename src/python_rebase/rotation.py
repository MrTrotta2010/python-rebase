"""Module that provides the Rotation class"""

# Copyright © 2023-2024 Tiago Trotta

# This file is part of PyReBase.

# PyReBase is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyReBase is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyReBase.  If not, see <https://www.gnu.org/licenses/>

class Rotation:
    """Represents a three-dimensional Rotation"""

    def __init__(self, x: int | float = None, y: int | float = None, z: int | float = None):
        self.x = x or 0
        self.y = y or 0
        self.z = z or 0

    def __eq__(self, other):
        return isinstance(other, Rotation) and self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return f'[{round(self.x, 4)}, {round(self.y, 4)}, {round(self.z, 4)}]'

    def to_list(self):
        """Converts a Rotation to a list"""

        return [self.x, self.y, self.z]

    def to_tuple(self):
        """Converts a Rotation to a tuple"""

        return (self.x, self.y, self.z)

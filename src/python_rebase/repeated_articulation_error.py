"""Module that provides the RepeatedArticulationError class"""

# Copyright © 2023 Tiago Trotta

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

class RepeatedArticulationError(Exception):
    """Error thrown when an articulation list has repeated articulations"""

    def __init__(self, art: str, art_list: list, *args):
        super().__init__(args)
        self.art = art
        self.art_list = art_list

    def __str__(self):
        return f'Duplicate articulation \'{self.art}\' in list {self.art_list}'

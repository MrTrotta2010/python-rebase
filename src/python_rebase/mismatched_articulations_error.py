"""Module that provides the MismatchedArticulationsError class"""

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

class MismatchedArticulationsError(Exception):
    """Error thrown when two articulation lists do not match"""
    def __init__(self, list_1: list, list_2: list, *args):
        super().__init__(args)
        self.list_1 = list_1
        self.list_2 = list_2

    def __str__(self):
        return f'Articulation lists do not match: {self.list_1} and {self.list_2}'

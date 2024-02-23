"""Module that provides the RepeatedArticulationError class"""

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

class UnauthorizedUserError(Exception):
    """Error thrown when an user can't be authenticated"""

    def __init__(self, user_mail: str, auth_token: list, *args):
        super().__init__(args)
        self.user_mail = user_mail
        self.auth_token = auth_token

    def __str__(self):
        return f"Couldn't authenticate user with e-mail '{self.user_mail}' and token '{self.auth_token}'"

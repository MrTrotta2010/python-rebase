"""Module that provides the Movement class"""

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

from json import dumps

from .register import Register
from .util import is_valid_movement_field, exclude_keys_from_dict, validate_initialization_dict
from .mismatched_articulations_error import MismatchedArticulationsError

FIELDS = { 'id': None, '_id': None, 'label': None, 'description': None, 'device': None,
          'articulations': None, 'fps': None, 'duration': None, 'numberOfRegisters': None,
          'insertionDate': None, 'updateDate': None, 'sessionId': None, 'professionalId': None,
          'patientId': None, 'appCode': None, 'appData': None, 'registers': None,
          'app': { 'code': None, 'data': None } }

class Movement:
    """Represents a ReBase Movement"""

    def __init__(self, properties_dict: dict = None):
        if properties_dict is None: properties_dict = {}
        self.__validate_movement_dict(properties_dict)

        self.id = properties_dict.get('id') or properties_dict.get('_id')
        self.label = properties_dict.get('label')
        self.description = properties_dict.get('description')
        self.device = properties_dict.get('device')
        self.articulations = properties_dict.get('articulations')
        self.fps = properties_dict.get('fps')
        self.duration = properties_dict.get('duration')
        self.number_of_registers = properties_dict.get('numberOfRegisters')
        self.insertion_date = properties_dict.get('insertionDate')
        self.update_date = properties_dict.get('updateDate')
        self.session_id = properties_dict.get('sessionId')
        self.professional_id = properties_dict.get('professionalId')
        self.patient_id = properties_dict.get('patientId')
        self.app_code = properties_dict.get('appCode') or properties_dict.get('app', {}).get('code')
        self.app_data = properties_dict.get('appData') or properties_dict.get('app', {}).get('data')

        if 'registers' in properties_dict:
            self._registers = self.__force_registers(properties_dict['registers'])
            if self.number_of_registers is None:
                self.__update_data(len(self._registers))
        else:
            self._registers = []

    def __str__(self):
        return str(self.to_dict())

    def __get_registers(self):
        return self._registers

    def __set_registers(self, data: list):
        if not isinstance(data, list): return

        self._registers = self.__force_registers(data)
        self.__update_data(len(data))

    registers = property(__get_registers, __set_registers)

    def add_register(self, register: Register) -> None:
        """Adds a Register to the register list (registers)"""

        if not isinstance(register, Register): register = Register(register)

        if self.articulations is None and (self.number_of_registers is None or self.number_of_registers == 0):
            self.articulations = register.articulations

        else:
            self.__validate_articulations(register.articulations)

        self._registers.append(register)
        self.__update_data(self.number_of_registers + 1 if self.number_of_registers is not None else 1)

    def to_dict(self, exclude: list = None) -> dict:
        """Converts the Movement to a dictionary. Receives a list of attributes to be ignored"""

        dictionary = {}
        if self.id is not None: dictionary['id'] = self.id
        if self.label is not None: dictionary['label'] = self.label
        if self.description is not None: dictionary['description'] = self.description
        if self.device is not None: dictionary['device'] = self.device
        if self.articulations is not None: dictionary['articulations'] = self.articulations
        if self.fps is not None: dictionary['fps'] = self.fps
        if self.duration is not None: dictionary['duration'] = self.duration
        if self.number_of_registers is not None: dictionary['numberOfRegisters'] = self.number_of_registers
        if self.insertion_date is not None: dictionary['insertionDate'] = self.insertion_date
        if self.update_date is not None: dictionary['updateDate'] = self.update_date
        if self.session_id is not None: dictionary['sessionId'] = self.session_id
        if self.professional_id is not None: dictionary['professionalId'] = self.professional_id
        if self.patient_id is not None: dictionary['patientId'] = self.patient_id

        if self.app_code is not None or self.app_data is not None: dictionary['app'] = {}
        if self.app_code is not None: dictionary['app']['code'] = self.app_code
        if self.app_data is not None: dictionary['app']['data'] = self.app_data

        if self.registers is not None and len(self.registers) > 0:
            dictionary['registers'] = [register.to_dict() for register in self.registers]

        exclude_keys_from_dict(dictionary, exclude)

        return dictionary

    def to_json(self, update: bool = False) -> str:
        """Converts the Movement to a json as expected by the ReBase Server.
        Receives a boolean that indicates wether the json will be used for an update"""

        exclude = ['id', 'insertionDate', 'updateDate', 'professionalId', 'patientId',
                   'articulations']
        if update: exclude += ['numberOfRegisters', 'duration', 'registers']

        return dumps({ 'movement': self.to_dict(exclude=exclude) })

    def __force_registers(self, data: list) -> list:
        array = []
        for register in data:
            r = register if isinstance(register, Register) else Register(register)
            if self.articulations is None:
                self.articulations = r.articulations
            else:
                self.__validate_articulations(r.articulations)
            array.append(r)

        return array

    # Atualiza os valores de number_of_registers e duration
    def __update_data(self, number_of_registers: int = 0) -> None:
        self.number_of_registers = number_of_registers
        if self.fps is not None and self.fps != 0:
            self.duration = self.number_of_registers / self.fps

    def __validate_articulations(self, articulations: list) -> None:
        if not self.__compare_articulation_lists(self.articulations, articulations):
            raise MismatchedArticulationsError(self.articulations, articulations)

    def __compare_articulation_lists(self, list_a: list, list_b: list) -> bool:
        if (list_a is None and list_b is not None) or (list_a is not None and list_b is None):
            return False

        length = len(list_a)
        if length != len(list_b):
            return False

        for i in range(length):
            if list_a[i] != list_b[i]:
                return False

        return True

    def __validate_movement_dict(self, dictionary: dict) -> None:
        validate_initialization_dict(is_valid_movement_field, 'Movement', FIELDS, dictionary)

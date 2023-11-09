"""Module that provides utility functions"""

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

def is_valid_str(string) -> bool:
    """Checks wether a given string is valid"""

    return isinstance(string, str)

def is_valid_number(number) -> bool:
    """Checks wether a given number is valid"""

    return isinstance(number, (int, float))

def is_valid_id(attribute) -> bool:
    """Checks wether a given id is valid"""

    return (is_valid_str(attribute) and attribute != '') or (is_valid_number(attribute) and attribute != 0)

def is_valid_movement_field(field: str, value: any) -> bool:
    """Checks wether a given field-value pair is valid for a Movement object"""

    if field in ['id', '_id', 'sessionId', 'professionalId', 'patientId', 'appCode']:
        return is_valid_id(value)
    if field in ['label', 'description', 'device', 'insertionDate', 'updateDate']:
        return is_valid_str(value)
    if field in ['fps', 'duration', 'numberOfRegisters']:
        return is_valid_number(value)
    if field in ['articulations', 'registers']:
        return isinstance(value, list)
    return field == 'appData'

def is_valid_session_field(field: str, value: any) -> bool:
    """Checks wether a given field-value pair is valid for a Session object"""

    if field in ['id', '_id', 'professionalId', 'patientId', 'patient.id']:
        return is_valid_id(value)
    if field in ['title', 'description', 'insertionDate', 'updateDate', 'mainComplaint',
                 'historyOfCurrentDisease', 'historyOfPastDisease', 'diagnosis',
                 'relatedDiseases', 'medications', 'physicalEvaluation',
                 'medicalData.mainComplaint', 'medicalData.historyOfCurrentDisease',
                 'medicalData.historyOfPastDisease', 'medicalData.diagnosis',
                 'medicalData.relatedDiseases', 'medicalData.medications',
                 'medicalData.physicalEvaluation']:
        return is_valid_str(value)
    if field in ['patientSessionNumber', 'patientAge', 'patientHeight', 'patientWeight',
                 'numberOfMovements', 'patient.age', 'patient.height', 'patient.weight']:
        return is_valid_number(value)
    if field == 'movements':
        return isinstance(value, list)
    return False

def exclude_keys_from_dict(dictionary: dict, keys: list):
    """Excludes a given list of keys from a dictionary"""

    if keys is not None:
        for key in keys:
            if key in dictionary:
                del dictionary[key]

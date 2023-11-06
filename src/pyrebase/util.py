"""Module that provides utility functions"""

def is_valid_str(string) -> bool:
    """Checks wether a given string is valid"""

    return isinstance(string, str)

def is_valid_number(number) -> bool:
    """Checks wether a given number is valid"""

    return isinstance(number, int) or isinstance(number, float)

def is_valid_id(attribute) -> bool:
    """Checks wether a given id is valid"""

    return (is_valid_str(attribute) and attribute != '') or (is_valid_number(attribute) and attribute != 0)

def is_valid_movement_field(field: str, value: any) -> bool:
    """Checks wether a given field-value pair is valid for a Movement object"""

    if field == 'id': return is_valid_id(value)
    if field == '_id': return is_valid_id(value)
    if field == 'label': return is_valid_str(value)
    if field == 'description': return is_valid_str(value)
    if field == 'device': return is_valid_str(value)
    if field == 'articulations': return isinstance(value, list)
    if field == 'fps': return is_valid_number(value)
    if field == 'duration': return is_valid_number(value)
    if field == 'numberOfRegisters': return is_valid_number(value)
    if field == 'insertionDate': return is_valid_str(value)
    if field == 'updateDate': return is_valid_str(value)
    if field == 'sessionId': return is_valid_id(value)
    if field == 'professionalId': return is_valid_id(value)
    if field == 'patientId': return is_valid_id(value)
    if field == 'appCode': return is_valid_id(value)
    if field == 'appData': return True
    if field == 'registers': return isinstance(value, list)
    return False

def is_valid_session_field(field: str, value: any) -> bool:
    """Checks wether a given field-value pair is valid for a Session object"""

    if field == 'id': return is_valid_id(value)
    if field == '_id': return is_valid_id(value)
    if field == 'title': return is_valid_str(value)
    if field == 'description': return is_valid_str(value)
    if field == 'professionalId': return is_valid_id(value)
    if field == 'patientSessionNumber': return is_valid_number(value)
    if field == 'insertionDate': return is_valid_str(value)
    if field == 'updateDate': return is_valid_str(value)
    if field == 'patientId': return is_valid_id(value)
    if field == 'patientAge': return is_valid_number(value)
    if field == 'patientHeight': return is_valid_number(value)
    if field == 'patientWeight': return is_valid_number(value)
    if field == 'mainComplaint': return is_valid_str(value)
    if field == 'historyOfCurrentDisease': return is_valid_str(value)
    if field == 'historyOfPastDisease': return is_valid_str(value)
    if field == 'diagnosis': return is_valid_str(value)
    if field == 'relatedDiseases': return is_valid_str(value)
    if field == 'medications': return is_valid_str(value)
    if field == 'physicalEvaluation': return is_valid_str(value)
    if field == 'numberOfMovements': return is_valid_number(value)
    if field == 'movements': return isinstance(value, list)

    if field == 'patient.id': return is_valid_id(value)
    if field == 'patient.age': return is_valid_number(value)
    if field == 'patient.height': return is_valid_number(value)
    if field == 'patient.weight': return is_valid_number(value)

    if field == 'medicalData.mainComplaint': return is_valid_str(value)
    if field == 'medicalData.historyOfCurrentDisease': return is_valid_str(value)
    if field == 'medicalData.historyOfPastDisease': return is_valid_str(value)
    if field == 'medicalData.diagnosis': return is_valid_str(value)
    if field == 'medicalData.relatedDiseases': return is_valid_str(value)
    if field == 'medicalData.medications': return is_valid_str(value)
    if field == 'medicalData.physicalEvaluation': return is_valid_str(value)

    return False

def exclude_keys_from_dict(dictionary: dict, keys: list):
    """Excludes a given list of keys from a dictionary"""

    if keys is not None:
        for key in keys:
            if key in dictionary:
                del dictionary[key]

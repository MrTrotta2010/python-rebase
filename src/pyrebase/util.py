def is_valid_str(string) -> bool:
  return isinstance(string, str) and len(string) > 0

def is_valid_number(number) -> bool:
  return isinstance(number, int) or isinstance(number, float)

def is_valid_id(attribute) -> bool:
  return is_valid_str(attribute) or is_valid_number(attribute)

def is_valid_movement_field(field: str, value: any) -> bool:
  if field == 'id': return is_valid_id(value)
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
  if field == 'articulationData': return isinstance(value, list)
  return False

def is_valid_session_field(field: str, value: any) -> bool:
  if field == 'id': return is_valid_id(value)
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
  return False

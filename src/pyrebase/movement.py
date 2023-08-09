from json import dumps

from .register import Register
from .mismatched_articulations_error import MismatchedArticulationsError

class Movement:
  def __init__(self, properties_dict: dict = {}):
    self.id = properties_dict.get('id')
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
    self.app_code = properties_dict.get('appCode')
    self.app_data = properties_dict.get('appData')

    if 'articulationData' in properties_dict:
      self._articulation_data = self.__force_registers(properties_dict['articulationData'])
      if self.number_of_registers is None: self.__update_data(len(self._articulation_data))
    else:
      self._articulation_data = []

  def __str__(self):
    return str(self.to_dict())

  def __get_articulation_data(self):
    return self._articulation_data

  def __set_articulation_data(self, data: list):
    if not isinstance(data, list): return

    self._articulation_data = self.__force_registers(data)
    self.__update_data(len(data))

  articulation_data = property(__get_articulation_data, __set_articulation_data)

  def add_register(self, register: Register) -> None:
    if not isinstance(register, Register): register = Register(register)

    if self.articulations is None and (self.number_of_registers is None or self.number_of_registers == 0):
      self.articulations = register.articulations

    else:
      self.__validate_articulation_data(register.articulations)

    self._articulation_data.append(register)
    self.__update_data(self.number_of_registers + 1 if self.number_of_registers is not None else 1)
  
  def to_dict(self, exclude: list = []) -> dict:
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

    if self.articulation_data is not None and len(self.articulation_data) > 0:
      dictionary['articulationData'] = { }
      first_register = True
      for register in self.articulation_data:
        for articulation in self.articulations:
          if first_register: dictionary['articulationData'][articulation] = []
          dictionary['articulationData'][articulation].append(register[articulation].to_array())
        first_register = False

    for key in exclude:
      if key in dictionary: del dictionary[key]

    return dictionary

  def to_json(self, update: bool = False) -> str:
    if update:
      return dumps(self.to_dict(exclude=['id', 'insertionDate', 'updateDate', 'numberOfRegisters', 'duration', 'articulationData', 'patientId', 'professionalId', 'articulations']))

    return dumps(self.to_dict(exclude=['id', 'professionalId', 'patientId', 'insertionDate', 'updateDate', 'articulations']))

  def __force_registers(self, data: list) -> list:
    array = []
    for register in data:
      r = register if isinstance(register, Register) else Register(register)
      self.__validate_articulation_data(r.articulations)
      array.append(r)

    return array

  # Atualiza os valores de number_of_registers e duration
  def __update_data(self, number_of_registers: int = 0):
    self.number_of_registers = number_of_registers
    if self.fps is not None and self.fps != 0: self.duration = self.number_of_registers / self.fps

  def __validate_articulation_data(self, articulations: list) -> None:
    if not self.__compare_articulation_lists(self.articulations, articulations):
      raise MismatchedArticulationsError(self.articulations, articulations)

  def __compare_articulation_lists(self, list_a: list, list_b: list) -> bool:
    if (list_a is None and list_b is not None) or (list_a is not None and list_b is None): return False

    length = len(list_a)
    if length != len(list_b): return False

    for i in range(length):
      if list_a[i] != list_b[i]: return False

    return True


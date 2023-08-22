from .util import is_valid_session_field
from json import dumps

FIELDS = ['id', 'title', 'description', 'professionalId', 'patientSessionNumber', 'insertionDate', 'updateDate', 'patientId',
          'patientAge', 'patientHeight', 'patientWeight', 'mainComplaint', 'historyOfCurrentDisease', 'historyOfPastDisease',
          'diagnosis', 'relatedDiseases', 'medications', 'physicalEvaluation', 'numberOfMovements', 'movements']

class Session:
  def __init__(self, properties_dict: dict = {}):
    self.__validate_session_dict(properties_dict)

    self.id = properties_dict.get('id')
    self.title = properties_dict.get('title')
    self.description = properties_dict.get('description')
    self.professional_id = properties_dict.get('professionalId')
    self.patient_session_number = properties_dict.get('patientSessionNumber')
    self.insertion_date = properties_dict.get('insertionDate')
    self.update_date = properties_dict.get('updateDate')
    self.patient_id = properties_dict.get('patientId')
    self.patient_age = properties_dict.get('patientAge')
    self.patient_height = properties_dict.get('patientHeight')
    self.patient_weight = properties_dict.get('patientWeight')
    self.main_complaint = properties_dict.get('mainComplaint')
    self.history_of_current_disease = properties_dict.get('historyOfCurrentDisease')
    self.history_of_past_disease = properties_dict.get('historyOfPastDisease')
    self.diagnosis = properties_dict.get('diagnosis')
    self.related_diseases = properties_dict.get('relatedDiseases')
    self.medications = properties_dict.get('medications')
    self.physical_evaluation = properties_dict.get('physicalEvaluation')
    self.number_of_movements = properties_dict.get('numberOfMovements')

    self.movements = properties_dict.get('movements') or []

  def __get_duration(self):
    duration = 0
    for movement in self.movements: duration += movement.duration
    return duration
  
  duration = property(__get_duration)

  def to_dict(self, exclude: list = []) -> dict:
    dictionary = {}
    if self.id is not None: dictionary['id'] = self.id
    if self.title is not None: dictionary['title'] = self.title
    if self.description is not None: dictionary['description'] = self.description
    if self.professional_id is not None: dictionary['professionalId'] = self.professional_id
    if self.patient_session_number is not None: dictionary['patientSessionNumber'] = self.patient_session_number
    if self.insertion_date is not None: dictionary['insertionDate'] = self.insertion_date
    if self.update_date is not None: dictionary['updateDate'] = self.update_date

    patient = {}
    if self.patient_id is not None: patient['id'] = self.patient_id
    if self.patient_age is not None: patient['age'] = self.patient_age
    if self.patient_height is not None: patient['height'] = self.patient_height
    if self.patient_weight is not None: patient['weight'] = self.patient_weight
    if len(patient) > 0: dictionary['patient'] = patient

    medical_data = {}
    if self.main_complaint is not None: medical_data['mainComplaint'] = self.main_complaint
    if self.history_of_current_disease is not None: medical_data['historyOfCurrentDisease'] = self.history_of_current_disease
    if self.history_of_past_disease is not None: medical_data['historyOfPastDisease'] = self.history_of_past_disease
    if self.diagnosis is not None: medical_data['diagnosis'] = self.diagnosis
    if self.related_diseases is not None: medical_data['relatedDiseases'] = self.related_diseases
    if self.medications is not None: medical_data['medications'] = self.medications
    if self.physical_evaluation is not None: medical_data['physicalEvaluation'] = self.physical_evaluation
    if len(medical_data) > 0: dictionary['medicalData'] = medical_data

    if self.number_of_movements is not None: dictionary['numberOfMovements'] = self.number_of_movements
    if self.movements is not None and len(self.movements) > 0:
      dictionary['movements'] = [movement.to_dict() for movement in self.movements]

    for key in exclude:
      if key in dictionary: del dictionary[key]

    return dictionary

  def to_json(self, update: bool = False) -> str:
    return dumps(self.to_dict(exclude=['id', 'insertionDate', 'updateDate', 'movements', 'numberOfMovements'] if update else ['id', 'insertionDate', 'updateDate']))

  def __str__(self):
    return str(self.to_dict())

  def __validate_session_dict(self, dictionary: dict) -> None:
    for key in dictionary.keys():
      if key not in FIELDS:
        raise ValueError(f"Invalid attribute in Session object: '{key}'")
      
      value = dictionary[key]
      if not is_valid_session_field(key, value):
        raise ValueError(f"Inappropriate value for attribute '{key}' in Session object: {type(value)} {value}")

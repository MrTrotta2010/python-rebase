from .movement import Movement
from .util import is_valid_str, is_valid_number, is_valid_attr
from json import dumps

class Session:
  def __init__(self, properties_dict: dict = {}):
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
    if is_valid_attr(self.id): dictionary['id'] = self.id
    if is_valid_str(self.title): dictionary['title'] = self.title
    if is_valid_str(self.description): dictionary['description'] = self.description
    if is_valid_attr(self.professional_id): dictionary['professionalId'] = self.professional_id
    if is_valid_number(self.patient_session_number): dictionary['patientSessionNumber'] = self.patient_session_number
    if is_valid_str(self.insertion_date): dictionary['insertionDate'] = self.insertion_date
    if is_valid_str(self.update_date): dictionary['updateDate'] = self.update_date

    patient = {}
    if is_valid_attr(self.patient_id): patient['id'] = self.patient_id
    if is_valid_number(self.patient_age): patient['age'] = self.patient_age
    if is_valid_number(self.patient_height): patient['height'] = self.patient_height
    if is_valid_number(self.patient_weight): patient['weight'] = self.patient_weight
    if len(patient) > 0: dictionary['patient'] = patient

    medical_data = {}
    if is_valid_str(self.main_complaint): medical_data['mainComplaint'] = self.main_complaint
    if is_valid_str(self.history_of_current_disease): medical_data['historyOfCurrentDisease'] = self.history_of_current_disease
    if is_valid_str(self.history_of_past_disease): medical_data['historyOfPastDisease'] = self.history_of_past_disease
    if is_valid_str(self.diagnosis): medical_data['diagnosis'] = self.diagnosis
    if is_valid_str(self.related_diseases): medical_data['relatedDiseases'] = self.related_diseases
    if is_valid_str(self.medications): medical_data['medications'] = self.medications
    if is_valid_str(self.physical_evaluation): medical_data['physicalEvaluation'] = self.physical_evaluation
    if len(medical_data) > 0: dictionary['medicalData'] = medical_data

    if is_valid_number(self.number_of_movements): dictionary['numberOfMovements'] = self.number_of_movements
    dictionary['movements'] = [movement.to_dict() for movement in self.movements]

    for key in exclude:
      if key in dictionary: del dictionary[key]

    return dictionary

  def to_json(self, update: bool = False) -> str:
    return dumps(self.to_dict(exclude=['id', 'insertionDate', 'updateDate', 'movements', 'numberOfMovements'] if update else ['id', 'insertionDate', 'updateDate']))

  def __str__(self):
    return str(self.to_dict())

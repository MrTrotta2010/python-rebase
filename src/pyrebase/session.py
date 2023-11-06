"""Module that provides the Session class"""

from json import dumps

from .movement import Movement
from .util import is_valid_session_field, exclude_keys_from_dict

FIELDS = { 'id': None, '_id': None, 'title': None, 'description': None, 'professionalId': None,
            'patientSessionNumber': None, 'insertionDate': None, 'updateDate': None,
            'patientId': None, 'patientAge': None, 'patientHeight': None, 'patientWeight': None,
            'mainComplaint': None, 'historyOfCurrentDisease': None, 'historyOfPastDisease': None,
            'diagnosis': None, 'relatedDiseases': None, 'medications': None,
            'physicalEvaluation': None, 'numberOfMovements': None, 'movements': None,
            'patient': {
                'id': None, 'age': None, 'height': None, 'weight': None
            },
            'medicalData': { 'mainComplaint': None, 'historyOfCurrentDisease': None,
                            'historyOfPastDisease': None, 'diagnosis': None,
                            'relatedDiseases': None, 'medications': None,
                            'physicalEvaluation': None
            }
        }

class Session:
    """Represents a ReBase Session"""

    def __init__(self, properties_dict: dict = None):
        if properties_dict is None: properties_dict = {}
        self.__validate_session_dict(properties_dict)

        self.id = properties_dict.get('id') or properties_dict.get('_id')
        self.title = properties_dict.get('title')
        self.description = properties_dict.get('description')
        self.professional_id = properties_dict.get('professionalId')
        self.patient_session_number = properties_dict.get('patientSessionNumber')
        self.insertion_date = properties_dict.get('insertionDate')
        self.update_date = properties_dict.get('updateDate')

        self.patient_id = properties_dict.get('patientId') or properties_dict.get('patient', {}).get('id')
        self.patient_age = properties_dict.get('patientAge') or properties_dict.get('patient', {}).get('age')
        self.patient_height = properties_dict.get('patientHeight') or properties_dict.get('patient', {}).get('height')
        self.patient_weight = properties_dict.get('patientWeight') or properties_dict.get('patient', {}).get('weight')

        self.main_complaint = properties_dict.get('mainComplaint') or properties_dict.get('medicalData', {}).get('mainComplaint')
        self.history_of_current_disease = properties_dict.get('historyOfCurrentDisease') or properties_dict.get('medicalData', {}).get('historyOfCurrentDisease')
        self.history_of_past_disease = properties_dict.get('historyOfPastDisease') or properties_dict.get('medicalData', {}).get('historyOfPastDisease')
        self.diagnosis = properties_dict.get('diagnosis') or properties_dict.get('medicalData', {}).get('diagnosis')
        self.related_diseases = properties_dict.get('relatedDiseases') or properties_dict.get('medicalData', {}).get('relatedDiseases')
        self.medications = properties_dict.get('medications') or properties_dict.get('medicalData', {}).get('medications')
        self.physical_evaluation = properties_dict.get('physicalEvaluation') or properties_dict.get('medicalData', {}).get('physicalEvaluation')

        self.movements = self.__force_movements(properties_dict['movements']) if 'movements' in properties_dict else []
        self.number_of_movements = properties_dict.get('numberOfMovements')

    def __get_duration(self):
        duration = 0
        for movement in self.movements:
            duration += movement.duration
        return duration

    duration = property(__get_duration)

    def to_dict(self, exclude: list = None, movement_exclude: list = None) -> dict:
        """Converts the Session to a dictionary. Receives a list of attributes to be ignored
        for the Session and a list of attributes to be ignored for it's Movements"""

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
            dictionary['movements'] = [movement.to_dict(exclude=movement_exclude) for movement in self.movements]

        exclude_keys_from_dict(dictionary, exclude)

        return dictionary

    def to_json(self, update: bool = False) -> str:
        """Converts the Session to a json as expected by the ReBase Server.
        Receives a boolean that indicates wether the json will be used for an update"""

        exclude = ['id', 'insertionDate', 'updateDate']
        movement_exclude = ['id', 'insertionDate', 'updateDate', 'professionalId', 'patientId',
                            'articulations']
        if update:
            exclude += ['movements', 'numberOfMovements']
            movement_exclude += ['numberOfRegisters', 'duration', 'registers']

        return dumps({ 'session': self.to_dict(exclude=exclude, movement_exclude=movement_exclude) })

    def __str__(self):
        return str(self.to_dict())

    def __validate_session_dict(self, dictionary: dict) -> None:
        for key in dictionary.keys():
            if key not in FIELDS:
                raise ValueError(f"Invalid attribute in Session object: '{key}'")

            if FIELDS[key] is None:
                value = dictionary[key]
                if not is_valid_session_field(key, value):
                    raise ValueError(f"Inappropriate value for attribute '{key}' in Session object: {type(value)} {value}")

            else:
                if not isinstance(dictionary[key], dict):
                    raise ValueError(f"Inappropriate value for attribute '{key}' in Session object: {type(dictionary[key])} {dictionary[key]}")

                for sub_key in dictionary[key].keys():
                    if sub_key not in FIELDS[key]:
                        raise ValueError(f"Invalid attribute in Session object: '{key}.{sub_key}'")

                    value = dictionary[key][sub_key]
                    if not is_valid_session_field(f'{key}.{sub_key}', value):
                        raise ValueError(f"Inappropriate value for attribute '{key}.{sub_key}' in Session object: {type(value)} {value}")

    def __force_movements(self, data: list) -> list:
        return [m if isinstance(m, Movement) else Movement(m) for m in data]

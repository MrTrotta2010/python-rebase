# pylint: disable=missing-module-docstring, missing-function-docstring

import pytest

from src.pyrebase.session import Session
from src.pyrebase.movement import Movement

class TestSession:
    def test_init(self):
        session = Session({ 'title': 'Test', 'id': 1 })

        assert session.title == 'Test'
        assert session.id == 1

    def test_init_error(self):
        with pytest.raises(ValueError):
            Session({ 'title': 'Test', 'invalid': 'key', 'id': 1 })

        with pytest.raises(ValueError):
            Session({ 'title': 2, 'id': {} })

        with pytest.raises(ValueError):
            Session({ 'patient': 'Joe' })

        with pytest.raises(ValueError):
            Session({ 'patient': { 'age': 'invalid' } })

        with pytest.raises(ValueError):
            Session({ 'patient': { 'age': 20, 'invalid': 'key' } })

        with pytest.raises(ValueError):
            Session({ 'medicalData': 'None' })

        with pytest.raises(ValueError):
            Session({ 'medicalData': { 'diagnosis': 0 } })

        with pytest.raises(ValueError):
            Session({ 'medicalData': { 'diagnosis': 'All right', 'invalid': 'key' } })

    def test_init_with_movement(self):
        movements = [
            Movement({ 'articulations': ['a1'], 'registers': [{ 'a1': [1, 2, 3] }], 'duration': 10 }),
            Movement({ 'articulations': ['a1'], 'registers': [{ 'a1': [1, 2, 3] }], 'duration': 10 })
        ]
        session = Session({ 'title': 'Test', 'id': 1, 'movements': movements })

        assert len(session.movements) == 2
        assert session.duration == movements[0].duration + movements[1].duration

    def test_init_with_movements_dict(self):
        movements = [
            { 'articulations': ['a1'], 'registers': [{ 'a1': [1, 2, 3] }], 'duration': 10 },
            { 'articulations': ['a1'], 'registers': [{ 'a1': [1, 2, 3] }], 'duration': 10 }
        ]
        session = Session({ 'title': 'Test', 'id': 1, 'movements': movements })
        assert len(session.movements) == 2
        assert isinstance(session.movements[0], Movement)
        assert isinstance(session.movements[1], Movement)

    def test_init_with_objects(self):
        session1 = Session({
            'patientId': 'Joe',
            'patientAge': 24,
            'patientHeight': 173,
            'patientWeight': 65,
            'mainComplaint': 'Pain',
            'historyOfCurrentDisease': 'Long',
            'historyOfPastDisease': 'Longer',
            'diagnosis': 'Bad.',
            'relatedDiseases': 'All of them',
            'medications': 'Same',
            'physicalEvaluation': 'Badder.'
        })
        session2 = Session({
            'patient': {
                'id': 'Joe',
                'age': 24,
                'height': 173,
                'weight': 65,
            },
            'medicalData': {
                'mainComplaint': 'Pain',
                'historyOfCurrentDisease': 'Long',
                'historyOfPastDisease': 'Longer',
                'diagnosis': 'Bad.',
                'relatedDiseases': 'All of them',
                'medications': 'Same',
                'physicalEvaluation': 'Badder.'
            }
        })

        assert session1.patient_id == session2.patient_id
        assert session1.patient_age == session2.patient_age
        assert session1.patient_height == session2.patient_height
        assert session1.patient_weight == session2.patient_weight
        assert session1.main_complaint == session2.main_complaint
        assert session1.history_of_current_disease == session2.history_of_current_disease
        assert session1.history_of_past_disease == session2.history_of_past_disease
        assert session1.diagnosis == session2.diagnosis
        assert session1.related_diseases == session2.related_diseases
        assert session1.medications == session2.medications
        assert session1.physical_evaluation == session2.physical_evaluation

    def test_conversions(self):
        original_dict = { 'id': '0', 'title': 'test', 'patientId': 'foo', 'movements': [Movement({ 'label': 'move' })] }
        expected_str = "{'id': '0', 'title': 'test', 'patient': {'id': 'foo'}, 'movements': [{'label': 'move'}]}"
        expected_json = "{\"session\": {\"title\": \"test\", \"patient\": {\"id\": \"foo\"}, \"movements\": [{\"label\": \"move\"}]}}"
        expected_update_json = "{\"session\": {\"title\": \"test\", \"patient\": {\"id\": \"foo\"}}}"
        session = Session(original_dict)

        session_dict = session.to_dict()

        assert session_dict['id'] == original_dict['id']
        assert session_dict['title'] == original_dict['title']
        assert session_dict['patient']['id'] == original_dict['patientId']
        assert isinstance(session_dict['movements'], list)
        assert isinstance(session_dict['movements'][0], dict)
        assert session_dict['movements'][0]['label'] == 'move'

        assert str(session) == expected_str
        assert session.to_json(update=False) == expected_json
        assert session.to_json(update=True) == expected_update_json

# pylint: enable=missing-module-docstring, missing-function-docstring

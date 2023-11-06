"""Module that provides usage examples of the Session class"""
import sys
from src.pyrebase.session import Session
from src.pyrebase.movement import Movement
import src.pyrebase.rebase_client as rebase_client

sys.path.append('..')

session = Session({
	'title': 'NewAPITest',
	'description': 'This is an empty session',
	'professionalId': 'MrTrotta2010',
	'patientId': '007'
})

print('> Inserting an empty session')
response = rebase_client.insert_session(session)
print(f'Inserted: {response}', '\n')
if not response.has_data('session'):
    sys.exit(1)

print("> Now we can add a Movement to the Session we've just created")
session_id = response.get_data('session').id
movement = Movement({
	'label': 'NewAPITest',
	'fps': 30,
	'sessionId': session_id,
	'articulations': ['1', '2'],
	'registers': [{ '1': [1, 1, 1], '2': [2, 2, 2] }]
})
response = rebase_client.insert_movement(movement)
print(f'Inserted: {response}', '\n')
if not response.has_data('movement'):
    sys.exit(2)

print('> If we search for the Session, it will come with a Movement')
response = rebase_client.find_session(session_id)
print(f'Found? {response}', '\n')
if not response.has_data('session'):
    sys.exit(3)

print("> Now, let's delete both")
movement_id = response.get_data('session').movements[0].id
response = rebase_client.delete_session(session_id)
print(f'Deleted! {response}')

response = rebase_client.delete_movement(movement_id)
print(f'Deleted! {response}', '\n')

print('> We could create the Session with the Movement already inside')
session = Session({
	'title': 'NewAPITest',
	'description': 'This is an empty session',
	'professionalId': 'MrTrotta2010',
	'patientId': '007',
    'movements': [
        {
			'label': 'NewAPITest',
			'fps': 30,
			'sessionId': session_id,
			'articulations': ['1', '2'],
			'registers': [{ '1': [1, 1, 1], '2': [2, 2, 2] }]
		}
	]
})

print('Note that the movements will always be converted into Movement objects, \
which, in turn, will convert all register into Register objects:')
print('Type of movement:', type(session.movements[0]))
print('Type of register:', type(session.movements[0].registers[0]))

response = rebase_client.insert_session(session)
print(f'Inserted: {response}', '\n')
if not response.has_data('session'):
    sys.exit(4)

print("> Now, let's update this new Session")
print("If we update the Session's patientId or professionalId, \
the Movement's patientId and professionalId will be updated as well")
session = response.get_data('session')
session.patient_id = '008'
session.professional_id = 'MrTrotta2011'

response = rebase_client.update_session(session)
print(f'Updated: {response}', '\n')

print('> Listing all Sessions with these new ids')
response = rebase_client.fetch_sessions(professional_id=session.professional_id, patient_id=session.patient_id, per=1)
print(f'Downloaded: {response}', '\n')

if response.has_data('sessions'):
    print('> Downloaded sessions are already of Session class')
    for idx, downloaded_session in enumerate(response.get_data('sessions')):
        print(f'{idx + 1}:', type(downloaded_session))
        print(downloaded_session.to_dict(exclude=['movements']))

        print('And their movements are already of Movement class')
        for idx_m, downloaded_movement in enumerate(downloaded_session.movements):
            print(f'{idx_m + 1}:', type(downloaded_movement))
            print(downloaded_movement.to_dict(exclude=['registers']))

print("\n> We can delete both the Session and all it's movements by using the parameter 'deep'")
movement_id = session.movements[0].id
response = rebase_client.delete_session(session.id, deep=True)
print(f'Deleted: {response}', '\n')

print('> Now we are unable to find either')
response = rebase_client.find_session(session.id)
print(f'Found? {response}')
response = rebase_client.find_movement(movement_id)
print(f'Found? {response}')

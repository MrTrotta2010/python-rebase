"""Module that provides usage examples of the Movement class"""
import sys
from src.python_rebase.rebase_client import ReBaseClient
from src.python_rebase.movement import Movement
from src.python_rebase.register import Register
from src.python_rebase.rotation import Rotation

sys.path.append('..')

rebase_client = ReBaseClient('your@email.com', 'your_token')

movement = Movement({
	'label': 'NewAPITest',
	'fps': 30,
	'professionalId': 'MrTrotta2010',
	'articulations': ['1', '2']
})
movement.add_register(Register({ '1': Rotation(1, 1, 1), '2': Rotation(2, 2, 2) }))

print("> Let's insert a new Movement")
response = rebase_client.insert_movement(movement)
print(f'Inserted: {response}', '\n')
if not response.has_data('movement'):
    sys.exit(1)

print("> Now, let's update the Movement we've just created")
movement.id = response.get_data('movement').id
movement.description = 'Vamos atualizar pra ver o que acontece'
response = rebase_client.update_movement(movement)
print(f'Updated: {response}', '\n')

print('> We can try listing the most recent Movement')
response = rebase_client.fetch_movements(professional_id=movement.professional_id, patient_id=movement.patient_id, per=1)
print(f'Downloaded: {response}', '\n')

if response.has_data('movements'):
    print('> Downloaded movements are already of Movement class:')
    for idx, downloaded_movement in enumerate(response.get_data('movements')):
        print(f'{idx + 1}:', type(downloaded_movement))
        print(downloaded_movement.to_dict(exclude=['registers']))

print("\n> Now, it's time to delete this Movement")
response = rebase_client.delete_movement(movement.id)
print(f'Deleted! {response}', '\n')
deleted_id = response.get_data('deletedId')
if deleted_id is None:
    sys.exit(2)

print('> You will see that we are now unable to find it')
response = rebase_client.find_movement(deleted_id)
print(f'Found? {response}', '\n')

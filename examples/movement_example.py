import sys
sys.path.append('..')

from src.pyrebase.movement import Movement
from src.pyrebase.register import Register
from src.pyrebase.rotation import Rotation

import src.pyrebase.rebase_client as rebase_client


movement = Movement({
	'label': 'NewAPITest',
	'fps': 30,
	'professionalId': 'MrTrotta2010',
	'articulations': ['1', '2']
})

movement.add_register(Register({ '1': Rotation(1, 1, 1), '2': Rotation(2, 2, 2) }))

## Insert
response = rebase_client.insert_movement(movement)
print(f'Inserted: {response}')

## Update
if not response.has_data('movement'): sys.exit(1)

movement.id = response.get_data('movement').id
movement.description = 'Vamos atualizar pra ver o que acontece'
response = rebase_client.update_movement(movement)
print(f'Updated: {response}')

## Delete
response = rebase_client.delete_movement(movement.id)
print(f'Deleted! {response}')

## Find
deleted_id = response.get_data('deletedId')
if deleted_id is None: sys.exit(2)

response = rebase_client.find_movement(deleted_id)
print(f'Found? {response}')

# List
response = rebase_client.fetch_movements(professional_id=movement.professional_id, patient_id=movement.patient_id, per=2)
print(f'\nDownloaded: {response}')

if response.has_data('movements'):
	print('> Downloaded movements are already of Movement class') 
	for idx, downloaded_movement in enumerate(response.get_data('movements')):
		print(f'\n{idx + 1}:', type(downloaded_movement))
		print(response.get_data('movements')[0].to_dict(exclude=['registers']))

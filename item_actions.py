from readmap import *
from readitems import *

def use_sonic(item1, item2):
	print('Bzzzzzzzz!')
def use_id(item1, item2):
	print('Bloop! The LED turns from red to green, you\'re now registered in C/2.04-5')
def use_biscuits(item1, item2):
	print('Nom! Nom! Nom!')
def drop_biscuits(item_id):
	return_item(item_id)['description'] = 'Inside, a crumbly mess without any texture what-so-ever.' 
actions = {
	'sonic_screwdriver': {'use': use_sonic, 'drop': None, 'take': None},
	'id': {'use': use_id, 'drop': None, 'take': None},
	'biscuits': {'use': use_biscuits, 'drop': drop_biscuits, 'take': None}
}
def return_action(item_id, action):
	for item, itemactions in actions.items():
		if item.replace('_', '') == item_id and itemactions[action] != None:
			return itemactions[action]

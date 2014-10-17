from readstory import *
def take_sonic(item_id):
	rooms['the TARDIS']['description'] = 'While Clara is screaming in despair, you manage to grab the screwdriver but if we don\'t do something soon, \nthe TARDIS could drop out of the time vortex and we need to land. Sparks are flying off the console.'
def use_sonic(item1, item2):
    rooms['the TARDIS']['description'] = 'The lights slowly fade up and the TARDIS starts to move in the time vortex again. gravity has been re-established \nwhich leaves Clara falling onto herself. Luckily for you, you landed on your feet. Suddenly,\n\n*Boom*\n\nThe TARDIS lands and makes you seem suspictious. \nWhy would the TARDIS just land without my control? Clara in excitement shouts "Let\'s go explore!" and runs out the door. \nWell, what are you waiting for?'
    return_item('psychicpaper')['give'] = True
    return_item('jellybabies')['give'] = True
    rooms['the TARDIS']['exits']['outside'] = "the Queen's Arcade"
    global objective
    objective = 'Find out what\'s happening'
    fix_exits()
def use_id(item1, item2):
	print('Bloop! The LED turns from red to green, you\'re now registered in C/2.04-5')
def use_biscuits(item1, item2):
	print('Nom! Nom! Nom!')
def drop_biscuits(item_id):
	return_item(item_id)['description'] = 'Inside, a crumbly mess without any texture what-so-ever.' 
actions = {
	'sonic_screwdriver': {'use': use_sonic, 'drop': None, 'take': take_sonic},
	'id': {'use': use_id, 'drop': None, 'take': None},
	'biscuits': {'use': use_biscuits, 'drop': drop_biscuits, 'take': None}
}
def return_action(item_id, action):

	for item, itemactions in actions.items():
		if item.replace('_', '') == item_id and action in itemactions.keys():

			return itemactions[action]

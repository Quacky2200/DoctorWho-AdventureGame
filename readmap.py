import xml.etree.ElementTree as ET
converses = {'north':'south', 'east':'west', 'up':'down', 'left':'right'}
rooms = []

def return_xml_items(room):
	items = []
	for itemdict in [room[i] for i in range(len(room)) if room[i].tag == 'item']:
		tempitem = {}
		for x,y in itemdict.items():
			tempitem[x] = y
		tempitem['description'] = itemdict.text
		items.append(tempitem)
	return items
def return_xml_exits(room):
	exits = {}
	for exitdict in [room[i] for i in range(len(room)) if room[i].tag == 'exit']:
		exits[exitdict.attrib['direction']] = exitdict.attrib['room']
	return exits
def return_converse(text):
	""" This function allows us to return the reverse of a direction 
	such as North is the converse of South. It has to use the converses dictionary 
	so you can add your own. For Example:
	>>> return_converse('north')
	'south'
	>>> return_converse('up')
	'down'
	>>> return_converse('')

	"""
	if text in converses.keys():
		return list(converses.values())[list(converses.keys()).index(text)]
	elif text in converses.values():
		return list(converses.keys())[list(converses.values()).index(text)]
def fix_exits():
	for room in rooms:
		for direction, leads_to in room['exits'].items():
			for roomtest in rooms:
				if roomtest['name'] == leads_to and not return_converse(direction) in roomtest['exits'].keys():
					roomtest['exits'][return_converse(direction)] = room['name']
def room_exists(room_id):
	""" Checks to see if a room exists.
	For example:
	>>> room_exists('Reception')
	True
	"""
	return room_id in [room['name'] for room in rooms]
def return_room(room_id):
	if room_exists(room_id):
		return list([room for room in rooms if room['name'] == room_id])[0]
def print_item_location(item_id):
	for room in rooms:
		for item in room['items']:
			if item['name'].replace('_','') == item_id:
				print('The ' + item['name'] + ' can be found in ' + (room['dir_name'] + ' ' if room['dir_name'] != '' else '') + room['name'])
				return
	print('The \'' + item_id + '\' cannot be found')
def return_room_from_exits(exits):
	#
	return list([room for room in rooms if room['exits'] == exits])[0]
def return_rooms():
	tree = ET.parse('map.xml')
	xml = tree.getroot()
	for room in xml:
		temproom = {'description': room.text}
		for attributes, values in room.attrib.items():
			temproom[attributes] = values
		temproom['exits'] = return_xml_exits(room)
		temproom['items'] = return_xml_items(room)
		rooms.append(temproom)
	fix_exits()
def exit_leads_to(exits, direction):
	#
	return return_room_from_exits(exits)['exits'][direction]
def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:

    >>> is_valid_exit(rooms["Reception"]["exits"], "south")
    True
    >>> is_valid_exit(rooms["Reception"]["exits"], "up")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "west")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "east")
    True
    """
    return chosen_exit in exits
def move_room(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:

    >>> move(rooms["Reception"]["exits"], "south") == rooms["Robs"]
    True
    >>> move(rooms["Reception"]["exits"], "east") == rooms["Tutor"]
    True
    >>> move(rooms["Reception"]["exits"], "west") == rooms["Office"]
    False
    """
    return return_room(return_room_from_exits(exits)['exits'][direction])

return_rooms()
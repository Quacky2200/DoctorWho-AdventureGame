import xml.etree.ElementTree as ET
import uuid
converses = {'north':'south', 'east':'west', 'up':'down', 'left':'right', 'inside':'outside', 'upstairs':'downstairs'}
rooms = {}

def return_xml_items(room):
	items = []
	tempitem = {}
	for xmlitems in [room[i] for i in range(len(room)) if room[i].tag == 'item']:
		tempitem = {'description': xmlitems.text}
		for attribute, value in xmlitems.items():
			tempitem[attribute] = (value if not (value.lower() == 'true') and not (value.lower() == 'false') else (True if value.lower() == 'true' else False))
		items.append(tempitem)
	return items
def return_xml_exits(room):
	exits = {}
	for exitdict in [room[i] for i in range(len(room)) if room[i].tag == 'exit']:
		exits[exitdict.attrib['direction']] = exitdict.attrib['room']
	return exits
def return_xml_characters(room):
	characters = []
	for characterdict in [room[i] for i in range(len(room)) if room[i].tag == 'character']:
		tempcharacter = {'name':characterdict.attrib['name'], 'description':characterdict.text}
		tempcharacter['items'] = return_xml_items(characterdict)
		characters.append(tempcharacter)
	return characters
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
		for direction, leads_to in rooms[room]['exits'].items():
			if not return_converse(direction) in rooms[leads_to]['exits']:
				rooms[leads_to]['exits'][return_converse(direction)] = room
def room_exists(room_id):
	return room_id in rooms.keys()
def return_room(room_id):
	if room_exists(room_id):
		return rooms[room_id]
def print_item_location(item_id):
	for room in rooms:
		for item in room['items']:
			if item['name'].replace('_','') == item_id and item['take']:
				print('The ' + item['name'].replace('_', ' ') + ' can be found in ' + (room['dir_name'] + ' ' if room['dir_name'] != '' else '') + room['name'])
				return
	print('The \'' + item_id + '\' cannot be found')
def return_rooms(xmlmap):
	for room in xmlmap:
		temproom = {'description': room.text}
		for attributes, value in room.attrib.items():
			temproom[attributes] = (value if not (value.lower() == 'true') and not (value.lower() == 'false') else (True if value.lower() == 'true' else False))
		temproom['exits'] = return_xml_exits(room)
		temproom['items'] = return_xml_items(room)
		temproom['characters'] = return_xml_characters(room)
		rooms[room.attrib['name']] = temproom
	fix_exits()
def exit_leads_to(exits, direction):
	return exits[direction]
def is_valid_exit(exits, chosen_exit):
    return chosen_exit in exits
def move_room(exits, direction):
    return rooms[exits[direction]]


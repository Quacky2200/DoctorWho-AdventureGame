import xml.etree.ElementTree as ET
from player import *

def return_items():
	tree = ET.parse('items.xml')
	xml = tree.getroot()
	for xmlitems in xml:
		tempitem = {'description': xmlitems.text}
		for attribute, value in xmlitems.items():
			tempitem[attribute] = (value if not (value.lower() == 'true') and not (value.lower() == 'false') else (True if value.lower() == 'true' else False))
		inventory.append(tempitem)
def item_exists(item_id):
	#
	return item_id in [item['name'].replace('_', '') for item in inventory]
def return_item(item_id):
	if item_exists(item_id):
		return list([item for item in inventory if item['name'].replace('_', '') == item_id])[0]
def weight_of_items(items):
    """This function takes a list of items and returns the total weight 
    from the whole list. Some of the items will be in grams and kilograms 
    and need to be translated into KG for the final total. The expected
    return result is a string. For Example:

    >>> weight_of_items([item_jelly_babies, item_psychic_paper])
    0.015

    >>> weight_of_items([])
    0

    """
    return sum([float(i['weight'].lower().replace('kg', '')) if 'kg' in i['weight'].lower() else float(i['weight'].lower().replace('g','')) / 1000 for i in items])
def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:

    >>> list_of_items([item_jelly_babies, item_psychic_paper])
    'psychic paper and a silver tin containing jelly babies'

    >>> list_of_items([item_sonic_screwdriver])
    'a sonic screwdriver'

    >>> list_of_items([])
    ''

    >>> list_of_items([item_money, item_handbook, item_laptop])
    'some money, a student handbook and a laptop'

    """
    result = ''
    for item in items:
        #Determine whether the item should be listed with 'a'/'an' or 'some'
        if item['name_type'] == 'group':
            result += 'some ' + item['name']
        elif item['name_type'] == 'pack':
            result += 'a pack of ' + item['name']
        elif item['name'][0] in ['a', 'e', 'i', 'o', 'u']:
            result += 'an ' + item['name']
        else:
            result += 'a ' + item['name']
        #If the item if the last one, put nothing, if second, finish with 'and' and otherwise, use a comma
        if item == items[len(items) - 1]:
            pass
        elif item == items[len(items) - 2]:
            result += ' and '
        else:
            result += ', '
    return result.replace('_', ' ')
return_items()

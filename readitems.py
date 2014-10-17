import xml.etree.ElementTree as ET
from player import *

def return_items(sentxmlitems):
	for xmlitems in sentxmlitems:
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
    return sum([float(i['weight'].lower().replace('kg', '')) if 'kg' in i['weight'].lower() else float(i['weight'].lower().replace('g','')) / 1000 for i in items])
def list_of_items(items):
    result = ''
    for item in items:
        #Determine whether the item should be listed with 'a'/'an' or 'some'
        if item['name_type'] == 'group':
            result += 'some ' + item['name']
        elif item['name_type'] == 'pack':
            result += 'a pack of ' + item['name']
        elif item['name_type'] == 'none':
            result += item['name']
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

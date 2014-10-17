from readmap import *
from readitems import *
tree = ET.parse('story.xml')
xml = tree.getroot()
for i in range(len(xml)):
	if xml[i].tag == 'map':
		return_rooms(xml[i])
	elif xml[i].tag == 'inventory':
		return_items(xml[i])
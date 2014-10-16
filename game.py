#!/usr/bin/python3
import sys
from parser import *
from characters import *
from time import sleep
import string

typewriter_enabled = False
typewriter_bypass = False
suggestions_enabled = True
inventorylist_enabled = True
help_enabled = True
story_history = ''

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
def typewriter(textbuffer, speed = 1):
    if not typewriter_bypass and typewriter_enabled:
        tw_char_speed = (0.025 / speed)
        tw_punct_speed = (tw_char_speed * 20)
        tw_char_final_speed = tw_char_speed
        tw_char_exhaustion_speed = tw_punct_speed / 1000
        for i in range(0, len(textbuffer)):
            print(textbuffer[i:(i+1)], end='',flush=True)
            if textbuffer[i:(i+1)] in [',', '?', '!'] and textbuffer[(i+1):(i+2)] == ' ' or textbuffer[i:(i+1)] == '.':
                tw_char_final_speed = tw_char_speed
                sleep(tw_punct_speed)
            else:
                tw_char_final_speed += tw_char_exhaustion_speed
                sleep(tw_char_final_speed)
        sleep(0.5)
        print("")
    else:
        print(textbuffer)
def item_in_inventory(item_id):
    return item_id in [item['id'].replace('_','') for item in inventory]

def return_item(item_id):
    if item_in_inventory(item_id): 
        return [item for item in inventory][ [item['id'].replace('_','') for item in inventory].index(item_id) ]

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
    # result = ''
    # for item in items:
    #     result += item['name'] + ("" if item == items[len(items) - 1] else (", " if not item == items[len(items) - 2] else " and "))
    # return result
    return ''.join([item['name'] + ("" if item == items[len(items) - 1] else (", " if not item == items[len(items) - 2] else " and ")) for item in items])

def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:

    >>> print_room_items(rooms["Test"])
    (nothing)

    >>> print_room_items(rooms["Office"])
    There is a pen here.
    <BLANKLINE>

    >>> print_room_items(rooms["Robs"])
    There is a power cable here.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.

    """
    if len(room['items']) != 0:
        typewriter("There is " + list_of_items(room['items']) + " here.\n")

def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:

    >>> print_inventory_items(inventory)
    You have an id card, a laptop and some money.
    <BLANKLINE>

    """

    typewriter("You have " + list_of_items(items) + ".")
    print("")

def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:

    >>> print_room(rooms["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>
    There is a pen here.
    <BLANKLINE>

    >>> print_room(rooms["Reception"])
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    You are in a maze of twisty little passages, all alike.
    Next to you is the School of Computer Science and
    Informatics reception. The receptionist, Matt Strangis,
    seems to be playing an old school text-based adventure
    game on his computer. There are corridors leading to the
    south and east. The exit is to the west.
    <BLANKLINE>
    There is a pack of biscuits and a student handbook here.
    <BLANKLINE>

    >>> print_room(rooms["Robs"])
    <BLANKLINE>
    ROBS' ROOM
    <BLANKLINE>
    You are leaning agains the door of the systems managers'
    room. Inside you notice Rob Evans and Rob Davies. They
    ignore you. To the north is the reception.
    <BLANKLINE>
    There is a power cable here.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    # if story_history != room['description']:
    #     typewriter_bypass = False
    # else:
    #     typewriter_bypass = True
    # story_history = room['description']
    # Display room name
    print("")
    typewriter(room["name"].upper() + (' - TUTORIAL' if tutorial else ''))
    print("")
    # Display room description
    typewriter(room["description"])
    print("")
    print_room_items(room)

def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:

    >>> exit_leads_to(rooms["Test"]["exits"], "")
    (nothing)
    >>> exit_leads_to(rooms["Reception"]["exits"], "east")
    "your personal tutor's office"
    >>> exit_leads_to(rooms["Tutor"]["exits"], "west")
    'Reception'
    """
    return rooms[exits[direction]]["name"]

def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:

    GO <EXIT NAME UPPERCASE> to <where it leads>.

    For example:
    >>> print_exit("east", "you personal tutor's office")
    GO EAST to you personal tutor's office.
    >>> print_exit("south", "Robs' room")
    GO SOUTH to Robs' room.
    """
    typewriter("GO " + direction.upper() + " to " + leads_to + ".")

def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print

    "TAKE <ITEM ID> to take <item name>."

    and for each item in the inventory print

    "DROP <ITEM ID> to drop <item name>."

    For example, the menu of actions available at the Reception may look like this:

    You can:
    GO EAST to your personal tutor's office.
    GO WEST to the parking lot.
    GO SOUTH to Robs' room.
    TAKE BISCUITS to take a pack of biscuits.
    TAKE HANDBOOK to take a student handbook.
    DROP ID to drop your id card.
    DROP LAPTOP to drop your laptop.
    DROP MONEY to drop your money.
    What do you want to do?

    """
    if suggestions_enabled:
        typewriter("You can:")
        # Iterate over available exits
        for direction in exits:
            # Print the exit name and where it leads to
            print_exit(direction, exit_leads_to(exits, direction))
        for item in room_items:
            if item['can_take']:
                typewriter('TAKE ' + item['id'].replace('_', '').upper() + ' to take ' + item['name'])
        for item in inv_items:
            if item['can_drop']:
                typewriter('DROP ' + item['id'].replace('_', '').upper() + ' to drop your ' + item['id'].replace('_', ' '))
        for item in inv_items:
            if item['can_use']:
                typewriter('USE ' + item['id'].replace('_', '').upper() + ' to use your ' + item['id'].replace('_', ' '))
        # print('\n'.join(['TAKE ' + item['id'].replace('_', '').upper() + ' to take ' + item['name'] for item in room_items if item['can_take']]))
        # print('\n'.join(['DROP ' + item['id'].replace('_', '').upper() + ' to drop your ' + item['id'].replace('_', ' ') for item in inv_items if item['can_drop']]))
        # print('\n'.join(['USE ' + item['id'].replace('_', '').upper() + ' to use your ' + item['id'].replace('_', ' ') for item in inv_items if item['can_use']]))
    print("What do you want to do?")

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

def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    global current_room
    if is_valid_exit(current_room['exits'], direction):
        current_room = move(current_room['exits'], direction)
    else:
        print("You cannot go there.")

def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """
    for item in current_room['items']:
        tempinventory = inventory[:]
        tempinventory.append(item)
        #print("Current weight: " + weight_of_items(inventory))
        #print("Weight with item: " + weight_of_items(tempinventory))
        #print("The maximum weight I can carry: " + str(max_weight))
        if item['id'].replace('_', '') == item_id and item['can_take'] and round(weight_of_items(tempinventory), 1) < max_weight:
            if item['takeaction'] != None: item['takeaction']()
            inventory.append(item)
            current_room['items'].remove(item)
            return
        elif item['id'].replace('_', '') == item_id and item['can_take'] and round(weight_of_items(tempinventory), 1) >= max_weight:
            print_wait("You struggle...", 2)
            break
    print_wait("You cannot take that.", 1)
    #If an item is there, put in inventory  

def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """
    for item in inventory:
        if item['id'].replace('_', '') == item_id and item['can_drop']:
            current_room['items'].append(item)
            inventory.remove(item)
            print_wait('My bag feels lighter')
            return 
    print_wait("You cannot drop that.")
    #drop inventory item if it's in the inventory and put in the current room 

def execute_use(item_id1, item_id2 = ''):
    item1 = return_item(item_id1)
    item2 = return_item(item_id2)
    if item1 != None:
        if item1['action'] != None: 
            items = item1['action'](item1, item2)

        else:
            print_wait('Nothing happens...', 0.8)
    else:
        print('You cannot use this.')
      
def execute_give(item_id, person):
    character = [char['action'] for char in current_room['characters'] if char['id'] == person or item_id][0] or None
    if character != None:
        character((return_item(item_id) if item_in_inventory(item_id) else return_item(person)))
    else:
        print('You cannot give that')

def execute_describe(item_id):
    item = return_item(item_id)
    if item != None:
        print(item['description'])
    elif len([char for char in current_room['characters'] if char['id'] == item_id]) > 0:
        print([char['description'] for char in current_room['characters'] if char['id'] == item_id][0])
    else:
        print("Descibe what?")

def execute_whereis(item_id):
    if item_in_inventory(item_id):
        print_wait('Your inventory contains ' + return_item(item_id)['name'],2.5)
        return
    else:
        for room in rooms.values():
            for item in room['items']:
                if item['id'].replace('_','') == item_id:
                    print_wait('Look in ' + room['name'])
                    return
    print_wait('I don\'t know where it is')

def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.

    """
    if len(command) == 0:
        print_wait('Nothing was entered...')
        return
    ########################################
    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print_wait("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print_wait("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print_wait("Drop what?")
    elif command[0] == "use":
        if len(command) == 3:
            execute_use(command[1], command[2])
        elif len(command) == 2:
            execute_use(command[1])
        else:
            print_wait("Use what?")
    elif command[0] == "give":
        if len(command) == 3:
            execute_give(command[1], command[2])
        elif len(command) == 2:
            print_wait('Give to whom?')
        else:
            print_wait('Give what?')
    elif command[0] == 'describe':
        if len(command) == 2:
            execute_describe(command[1])
        else:
            print_wait('Describe what?')
    elif command[0] == 'whereis':
        if len(command) > 1:
            execute_whereis(command[1])
        else:
            print('Where\'s What?')
    elif command[0] == 'inventory':
        print_inventory_items(inventory)
    elif command[0] == 'objective':
        print_wait(objective)
    elif command[0] == 'help' and help_enabled:
        print('HELP (:) optional\nTAKE [ITEM]\n   Put the item into your inventory\n   For example:\n   TAKE MANUAL\n   TAKE THE MANUAL\nDROP [ITEM]\n   Remove the item from your inventory\n   For example:\n   DROP MANUAL\nGIVE [ITEM] [PERSON]\n   Give an item to someone\n   For Example:\n   GIVE MANUAL TO ME\nUSE [ITEM] [:ITEM:]\n   Use the item or use the item with another (item)\n   For Example:\n   USE PEN ON MANUAL\nDESCRIBE [ITEM/CHARACTER]\n   Describing an item or character can help\n   For Example\n   DESCRIBE ME\n   \'You need help...\'\nQUIT\n   No need for help or example with this one.')
    elif command[0] == "quit":
        #Check if the player wants to continue, otherwise they risk losing their game progress accidentally.
        check = input("Quitting will not save game progress, continue? (Y/N): ")
        checkvalue = (check.split()[0].lower() if len(check) != 0 else execute_command(command))
        #Get the first word, we don't care about the others, and also make it lowercase (e.g. yEs PlEaSe = yes) 
        #if they entered something, otherwise, repeat the question
        if checkvalue == 'y' or checkvalue == 'yes': #We can now check the two values easily
            quit() #Only quit if they said yes
    else:
        print_wait("This makes no sense.")

def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.

    """

    # Display menu
    print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input

def move(exits, direction):
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

    # Next room to go to
    return rooms[exits[direction]]

# This is the entry point of our program
def main():

    # Main game loop
    while True:
        global typewriter_bypass
        global story_history
        if story_history == current_room['description']:
            typewriter_bypass = True
        else:
            typewriter_bypass = False
        story_history = current_room['description']
        # Display game status (room description, inventory etc.)
        print_room(current_room)
        print_inventory_items(inventory)

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)
        # Execute the player's command
        execute_command(command)



# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":
    global typewriter_enabled
    global suggestions_enabled
    global help_enabled
    global inventorylist_enabled
    start = True
    for arg in sys.argv:
        if arg == 'storymode':
            typewriter_enabled = True
        elif arg == 'nosuggest':
            suggestions_enabled = False
        elif arg == 'nohelp':
            help_enabled = False
        elif arg == 'noinvlist':
            inventorylist_enabled = False
        elif 'help' in arg or '?' in arg:
            start = False
            print('HELP:\nstorymode\n   Story mode uses a typewriter to help read the text slowly like in a book.\nnosuggest\n   Suggestions are provided to help the user throughout the story. Disabling this makes the game more interesting.\nnohelp\n   Help can usually be provided when \'help\' is inputted. Without it can make the game harder.\nnoinvlist\n   Normally, a list of your inventory such as \'You have an id card, a laptop and some money\' appears every time a command has been entered.\nhelp\n   Shows this help menu')
    if start: main()

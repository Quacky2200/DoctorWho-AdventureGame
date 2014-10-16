#!/usr/bin/python3
import sys
from gameparser import *
from item_actions import *
from time import sleep
current_room = return_room('Reception')
typewriter_enabled = False
typewriter_bypass = False
suggestions_enabled = True
inventorylist_enabled = True
help_enabled = True
story_history = ''

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

def print_wait(text, time = 1):
    print(text)
    sleep(time)

def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:

    >>> print_room_items(return_room('Reception'))
    There is a pack of biscuits here.
    <BLANKLINE>

    Note: <BLANKLINE> here means that doctest should expect a blank line.

    """
    if len(room['items']) != 0 and suggestions_enabled:
        typewriter("There is " + list_of_items(room['items']) + " here.")
        print("")

def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:

    >>> print_inventory_items(inventory)
    You have a laptop, an id, some money and a sonic screwdriver.
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

    >>> print_room(return_room("Reception"))
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    Reception is a nice place to live if you're a receptionist.
    Receptionists are cool.
    <BLANKLINE>
    There is a pack of biscuits here.
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
    typewriter(room["name"].upper())
    print("")
    # Display room description
    typewriter(room["description"])
    print("")
    print_room_items(room)

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
    print("GO " + direction.upper() + " to " + leads_to + ".")

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
            if item['take']:
                print('TAKE ' + item['name'].replace('_', '').upper() + ' to take ' + item['name'] + ".")
        for item in inv_items:
            if item['drop']:
                print('DROP ' + item['name'].replace('_', '').upper() + ' to drop your ' + item['name'].replace('_', ' ') + ".")
        for item in inv_items:
            if item['use']:
                print('USE ' + item['name'].replace('_', '').upper() + ' to use your ' + item['name'].replace('_', ' ') + ".")

def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    global current_room
    if is_valid_exit(current_room['exits'], direction):
        current_room = move_room(current_room['exits'], direction)
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
        if item['name'].replace('_', '') == item_id and item['take'] and round(weight_of_items(tempinventory), 1) < max_weight:
            action = return_action(item_id, 'take')
            if action != None: action(item_id)
            inventory.append(item)
            current_room['items'].remove(item)
            return
        elif item['name'].replace('_', '') == item_id and item['take'] and round(weight_of_items(tempinventory), 1) >= max_weight:
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
        if item['name'].replace('_', '') == item_id and item['drop']:
            action = return_action(item_id, 'drop')
            if action != None: action(item_id)
            current_room['items'].append(item)
            inventory.remove(item)
            print_wait('My bag feels lighter')
            return 
    print_wait("You cannot drop that.")
    #drop inventory item if it's in the inventory and put in the current room 

def execute_use(item_id1, item_id2 = ''):
    item1 = return_item(item_id1)
    item2 = return_item(item_id2)
    if item1 == None or item2 == None and item_id2 != '':
        print('You cannot use this.')
    else:
        action = return_action(item_id1, 'use')
        if action != None: action(item1, item2)
      
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
    # elif len([char for char in current_room['characters'] if char['id'] == item_id]) > 0:
    #     print([char['description'] for char in current_room['characters'] if char['id'] == item_id][0])
    else:
        print("Descibe what?")

def execute_whereis(item_id):
    if item_exists(item_id):
        print_wait('Your ' + return_item(item_id)['name'] + ' can be found in your inventory',2.5)
    else:
        print_item_location(item_id)

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
            if command[1] == 'room':
                print_room(current_room)
                return
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
    elif 'suggest' in command[0]:
        print_menu(current_room['exits'], current_room['items'], inventory)
    elif command[0] == 'help' and help_enabled:
        print('HELP (:) optional\nTAKE [ITEM]\n   Put the item into your inventory\n   For example:\n   TAKE MANUAL\n   TAKE THE MANUAL\nDROP [ITEM]\n   Remove the item from your inventory\n   For example:\n   DROP MANUAL\nGIVE [ITEM] [PERSON]\n   Give an item to someone\n   For Example:\n   GIVE MANUAL TO ME\nUSE [ITEM] [:ITEM:]\n   Use the item or use the item with another (item)\n   For Example:\n   USE PEN ON MANUAL\nDESCRIBE [ITEM/CHARACTER]\n   Describing an item,character or room can help\n   For Example\n   DESCRIBE ME\n   \'You need help...\'\nINVENTORY\n   Prints a list of your inventory out.\nOBJECTIVE\n   Prints the current objective out\nSUGGEST\n   Get quick suggestions when necessary\nQUIT\n   No need for help or example with this one.')
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
    if not typewriter_bypass: print_menu(exits, room_items, inv_items)

    # Read player's input
    user_input = input("What do you want to do?\n> ")

    # Normalise the input
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input

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
            print_room(current_room)
            # Display game status (room description, inventory etc.)
            if inventorylist_enabled: print_inventory_items(inventory)
        story_history = current_room['description']

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)
        # Execute the player's command
        execute_command(command)



# Are we being run as a script? If so, run main().
# '__main__' is the name of the scope in which top-level code executes.
# See https://docs.python.org/3.4/library/__main__.html for explanation
if __name__ == "__main__":

    start = True
    for arg in [args.lower() for args in sys.argv]:
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
            print('HELP:\nSTORYMODE\n   Story mode uses a typewriter function to allow the player to read.\nNOSUGGEST\n   Suggestions are provided to help the user throughout the story. Disabling this makes the game more interesting.\nNOHELP\n   Help can usually be provided when \'help\' is inputted. Without it can make the game harder.\nNOINVLIST\n   Normally, a list of your inventory such as \'You have an id card, a laptop and some money\' appears every time a command has been entered.\nHELP\n   Shows this help menu')
    if start: main()

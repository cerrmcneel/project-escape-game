# %%
# define rooms and items

couch = {
    "name": "couch",
    "type": "furniture",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

table = {
    "name": "table",
    "type": "furniture",
}

chair = {
    "name": "chair",
    "type": "furniture",
}

dead_men = {
    "name": "dead men",
    "type": "furniture",
}

picture = {
    "name": "picture",
    "type": "furniture",
}

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

door_d = {
    "name": "door d",
    "type": "door",
}

door_e = {
    "name": "door 5",
    "type": "door",
}

door_f = {
    "name": "door 6",
    "type": "code door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
     "name": "key for door d",
    "type": "key",
    "target": door_d,
}

key_e = {
    "name": "key for door 5",
    "type": "key",
    "target": door_e,
}

Code_f = {
    "name": "44",
    "type": "code",
    "target": door_f,
}

piano = {
    "name": "piano",
    "type": "furniture",
}
painting = {
    "name": "painting",
    "type": "furniture",
}

dining_table = {
    "name": "dining table",
    "type": "furniture",
}

safe = {
    "name": "safe",
    "type": "safe",
}
hidden_note = {
    "name": "note",
    "type": "note",
}

paper1 = {
    "name": "a paper that says: The key is in the picture",
    "type": "paper1",
    "target": picture
}

paper2 = {
    "name": """stuck in the door a paper that says: Final step to survive... Good luck.

    CODE:
    $ + $ + $ = 30
    & + 2$ = 24
    $ + & + @ = 20
    @ x @ - 2$ = &&
    
    && - $ = Code""",
    "type": "paper2",
} #i didt like this for less coding

game_room = {
    "name": "game room",
    "type": "room",
}

bedroom_1 = {
    'name':"bedroom 1",
    'type':'room'
}

bedroom_2 = {
    'name':"bedroom 2",
    'type':'room'
}

living_room = {
    'name':"living room",
    'type':'room'
}

escape_room = {    
    "name": "escape room",
    "type": "room",
} 

outside = {
  "name": "outside"
}

all_rooms = [game_room, bedroom_1, bedroom_2, living_room, escape_room, outside]#change outside to the end

all_doors = [door_a, door_b, door_c, door_d, door_e, door_f]

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "outside": [door_f],
    "bedroom 1": [door_a, door_c, queen_bed, door_b, painting],
    "door a": [game_room, bedroom_1],
    "door b": [bedroom_1, bedroom_2],
    "door c": [bedroom_1, living_room],
    "queen bed": [key_b],
    "bedroom 2": [double_bed, dresser, safe, door_b],
    "dresser": [key_d],
    "double bed": [],
    "living room": [door_d, dining_table],
    "door d": [living_room, outside],
    "painting": [hidden_note],
    "safe": [key_c],
    "living room": [table, chair, dead_men, picture, door_e],
    "escape room": [door_f, paper2],
    "dead men": [paper1],
    "picture": [key_e],
    "outside": [door_f],
    "door 5": [living_room, escape_room],
    "door 6": [escape_room, outside]
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "inventory": [],
    "target_room": outside
}

# %%
def linebreak():
    """
    Print a line break to separate game events visually.
    """
    print("\n\n")

def start_game():
    """
    Start the game. 
    Sets the initial context and intro story, then enters the main game loop.
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])

def play_room(room):
    """
    The main game loop logic for a specific room.
    1. Checks if the player has reached the target room (Victory Condition).
    2. If not, prompts the player for an action (explore, examine, inventory).
    """
    game_state["current_room"] = room
    
    # --- VICTORY CHECK ---
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        # --- MAIN ACTION LOOP ---
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine' or 'inventory'?").lower().strip()
        
        if intended_action == "explore":
            explore_room(room)
            play_room(room) # Reloads the room after exploring
            
        elif intended_action == "examine":
            # Passes user input directly to the examine function
            examine_item(input("What would you like to examine?").lower().strip())
            
        elif intended_action == "inventory":
            check_inventory()
            play_room(room) # Reloads room after checking pockets
            
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        
        linebreak()

def check_inventory():
    """
    Lists all items currently held by the player.
    """
    if len(game_state['inventory']) == 0:
        print('You have no keys in your inventory')
    else:
        output_message = 'You check your pockets and find the keys'
        print(output_message)
        for key in game_state['inventory']:
            print(key['name'])

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    Uses a loop to build a comma-separated string of items.
    """
    explore_message = "You explore the room. This is " + room["name"] + ". You find "
    for item in object_relations[room["name"]]:
        explore_message += str(item["name"]) + ", "
    
    # Removes the last comma and space, adds a period.
    explore_message = explore_message[:-2] + "." 
    print(explore_message)

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the second room (the one we are not currently in).
    """
    connected_rooms = object_relations[door["name"]]
    # Logic assumption: The door connects exactly two rooms.
    if current_room == connected_rooms[0]:
        return connected_rooms[1]
    else:   
        return connected_rooms[0]
def examine_item(item_name):    
    """
    The core interaction function.
    1. Compiles a list of everything the player can see (Room + Inventory).
    2. Loops through to find the matching item.
    3. Executes specific logic based on item type (Door, Safe, Note, Generic).
    """
    
    current_room = game_state["current_room"]
    
    # Combine room items and inventory so player can examine things in their pocket
    items_to_check = object_relations[current_room["name"]] + game_state["inventory"]
    
    next_room = ""
    output = None
    
    for item in items_to_check:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            
            # --- Door 6 CODE TO EXIT -----
            if(item["name"] == "door 6"):
                answer = input("Enter code: ")
                if answer == "6":
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "wrong code, try again"
            
            # --- DOOR LOGIC ---
            elif(item["type"] == "door"):
                have_key = False
                for key in game_state["inventory"]:
                    # BUG FIX: Added "target" in key check to prevent crashing on non-key items (like notes)
                    if("target" in key and key["target"] == item):
                        have_key = True
                
                if(have_key):
                    output += "You unlock it with a key you have. Now you can enter to the next room" # Added sentence to enter next room
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            
            # --- SAFE LOGIC ---
            elif item["type"] == "safe":
                output += "You examine the safe. It's a combination lock."
                code = input("Enter the combination to open the safe:")
                if code == "6596":
                    output += "The safe is now open."
                    # Check if safe has hidden items inside
                    if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                        item_found = object_relations[item["name"]].pop()
                        game_state["inventory"].append(item_found)
                        output += "You find " + item_found["name"] + "."
                else:
                    output += "The combination is incorrect."
            
            # --- NOTE LOGIC ---
            elif item["type"] == "note":
                output += "The note reads: 'I am the lists rigid sibling.\nYou can see what I hold,\nbut you can never change my mind.\n Wrap me in parentheses, and I'll keep your secrets forever\n"
                output += "Dictionary : 2076\n"
                output += "Tuple : 6596\n"
                output += "Set : 3448\n"    
            
            # --- GENERIC ITEM LOGIC (Hidden Objects) ---
            # If it's not a door, safe, or note, check if it hides something (like the piano or painting)
            elif (item["name"] in object_relations and len(object_relations[item["name"]])>0):
                item_found = object_relations[item["name"]].pop()
                game_state["inventory"].append(item_found)
                output += "You find " + item_found["name"] + "."
            
            # ---- LOGIC PAPER&PICTURE RELATION ----
            elif(item["name"] == "picture"):
                have_paper = False
                for paper in game_state["inventory"]:
                    if paper == "paper1":
                        have_paper = True
                if (have_paper):
                    if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                        item_found = object_relations[item["name"]].pop()
                        game_state["inventory"].append(key_e)
                        output += "You found the " + key_e["name"] + "."
                    else:
                        output += "There isn't anything interesting about it."
                else:
                    output += "There isn't anything interesting about it."
                
                #-----LOGIC IN DEAD MEN ----
            elif(item["name"] == "dead men"):
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["inventory"].append("paper1")
                    output += "You found a " + paper1["name"] + "."
                else:
                    output += "There isn't anything interesting about it."

            
            # --- NOTHING INTERESTING ---
            else:
                output += "There isn't anything interesting about it."
            
            # Print the result and exit loop once item is found
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    # --- ROOM TRANSITION ---
    # Only asks to move if a next_room was set (i.e., a door was unlocked)
    if(next_room and input("Do you want to go to the next room? enter 'yes' or 'no'").lower().strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)

# %%
game_state = INIT_GAME_STATE.copy()

start_game()

# %%




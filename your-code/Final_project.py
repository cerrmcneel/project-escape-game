import copy
import sys

#--------------------- ROOMS ----------------------------
game_room = {"name": "game room", "type": "room"}
music_room = {"name": "music room", "type": "room"}
bedroom_1 = {"name": "bedroom 1", "type": "room"}
bedroom_2 = {"name": "bedroom 2", "type": "room"}
living_room = {"name": "living room", "type": "room"}
escape_room = {"name": "escape room", "type": "room"}

#-------------------- ITEMS -----------------------------
couch = {"name": "couch", "type": "furniture"}
dining_table = {"name": "dining table", "type": "furniture"}
tv = {"name": "tv", "type": "furniture"}

carpet = {"name": "carpet", "type": "furniture"}
piano = {"name": "piano", "type": "furniture"}
guitar = {"name": "guitar", "type": "furniture"}
mona_lisa = {"name": "mona lisa", "type": "art"}

queen_bed = {"name": "queen bed", "type": "furniture"}
painting = {"name": "painting", "type": "furniture"}
safe = {"name": "safe", "type": "safe"}
dead_men = {"name": "dead men", "type": "furniture"}
picture = {"name": "picture", "type": "furniture"}

#--------------------- DOORS -----------------------------
door_a = {"name": "door a", "type": "door"}
door_b = {"name": "door b", "type": "door"}
door_c = {"name": "door c", "type": "door"}
door_d = {"name": "door d", "type": "door"}
door_e = {"name": "door e", "type": "door"}
door_f = {"name": "door f", "type": "code door"}

#----------------- KEYS ------------------------------
key_a = {"name": "key for door a", "type": "key", "target": door_a}
key_b = {"name": "key for door b", "type": "key", "target": door_b}
key_c = {"name": "key for door c", "type": "key", "target": door_c}
key_d = {"name": "key for door d", "type": "key", "target": door_d}
key_e = {"name": "key for door e", "type": "key", "target": door_e}

#--------------- OBJECT RELATIONS -----------------
object_relations = {
    "game room": [couch, dining_table, tv, door_a],
    "music room": [carpet, piano, guitar, mona_lisa, door_b],
    "bedroom 1": [queen_bed, painting, door_b, door_c, door_d],
    "bedroom 2": [safe, door_c],
    "living room": [dead_men, picture, door_d, door_e],
    "escape room": [door_f],
}

#------------- GAME STATE --------------------------
INIT_GAME_STATE = {
    "current_room": game_room,
    "inventory": [],
    "game_puzzle_progress": 0,
    "music_stage": 0,
    "music_used_items": set(),
    "notes": set(),
    "dead_men_examined": 0
}

game_state = copy.deepcopy(INIT_GAME_STATE)

#--------------- INPUT HANDLING -------------------
def safe_input(prompt):
    value = input(prompt).lower().strip()
    if value == "exit":
        sys.exit()
    return value

#-------------- ROOM EXPLORATION -----------------
def explore_room(room):
    print("\nYou see:")
    for item in object_relations[room["name"]]:
        print("-", item["name"])

#-------------- INVENTORY & NOTES -----------------
def check_inventory():
    if not game_state["inventory"] and not game_state["notes"]:
        print("Your inventory is empty.")
        return

    if game_state["inventory"]:
        print("You have:")
        for item in game_state["inventory"]:
            print("-", item["name"])

    if game_state["notes"]:
        print("\nNotes:")
        for note in game_state["notes"]:
            print(note)

#--------------- MUSIC ROOM PUZZLE -----------------
def solve_music_equation():
    if game_state["music_stage"] < 3:
        print("The equation is incomplete.")
        return

    try:
        answer = int(safe_input("Solve the equation: "))
    except ValueError:
        print("That doesn’t seem right.")
        return

    if answer == 16 and key_b not in game_state["inventory"]:
        print("🔑 You obtain a key.")
        game_state["inventory"].append(key_b)

#---------------- EXAMINE LOGIC -----------------
def examine_item(item_name):
    room = game_state["current_room"]

    if item_name not in [i["name"] for i in object_relations[room["name"]]]:
        print("That item is not here.")
        return None

    #----------- DOORS ----------------
    for door in [door_a, door_b, door_c, door_d, door_e]:
        if item_name == door["name"]:
            for key in game_state["inventory"]:
                if key["target"] == door:
                    return {
                        "door a": music_room,
                        "door b": bedroom_1,
                        "door c": bedroom_2,
                        "door d": living_room,
                        "door e": escape_room,
                    }[door["name"]]
            print("🚪 The door is locked.")
            return None

    #----------- GAME ROOM ----------------
    if room["name"] == "game room":
        order = ["couch", "dining table", "tv"]
        if item_name != order[game_state["game_puzzle_progress"]]:
            game_state["game_puzzle_progress"] = 0
            print("Wrong order.")
            return None

        game_state["game_puzzle_progress"] += 1
        print("Correct.")

        if item_name == "tv" and key_a not in game_state["inventory"]:
            game_state["inventory"].append(key_a)
            print("You found a key for door a.")

    #----------- MUSIC ROOM ----------------
    if room["name"] == "music room":
        if item_name == "mona lisa":
            solve_music_equation()
            return None

        if item_name in ("carpet", "piano", "guitar"):
            if item_name in game_state["music_used_items"]:
                print("You already examined this.")
                return None

            if game_state["music_stage"] == 0:
                game_state["music_stage"] = 1
                print("🧩 Equation: 8 /")

            elif game_state["music_stage"] == 1:
                game_state["music_stage"] = 2
                print("🧩 Equation: 8 / 2 *")

            elif game_state["music_stage"] == 2:
                print(
                    "🎸 A normal guitar has 6 strings.\n"
                    "🎸 Without 2 of them, you get the last number."
                )
                try:
                    value = int(safe_input("Enter the last number: "))
                except ValueError:
                    return None

                if value == 4:
                    game_state["music_stage"] = 3
                    print(
                        "✅ That completes the equation.\n"
                        "🧩 Equation: 8 / 2 * 4\n"
                        "🖼️ Now go to Mona Lisa to solve the code and discover the key she hides to leave this room."
                    )
                else:
                    print("❌ That number doesn’t fit.")
                    return None

            game_state["music_used_items"].add(item_name)

    #----------- BEDROOM 1 ----------------
    if room["name"] == "bedroom 1":
        if item_name == "queen bed" and key_c not in game_state["inventory"]:
            game_state["inventory"].append(key_c)
            print("🔑 You found a key.")

        if item_name == "painting":
            note = (
                "📝 Note:\n"
                "I am the list’s rigid sibling.\n"
                "You can see what I hold, but never change it.\n"
                "Tuple code: 6596"
            )
            game_state["notes"].add(note)
            print(note)

    #----------- BEDROOM 2 ----------------
    if room["name"] == "bedroom 2" and item_name == "safe":
        if any("6596" in n for n in game_state["notes"]):
            if safe_input("Enter safe code: ") == "6596":
                if key_d not in game_state["inventory"]:
                    game_state["inventory"].append(key_d)
                    print("🔓 Safe opens. You found a key for door d.")
        else:
            print("You need a hint.")

    #----------- LIVING ROOM ----------------
    if room["name"] == "living room":
        if item_name == "dead men":
            game_state["dead_men_examined"] += 1

            if game_state["dead_men_examined"] == 1:
                print(
                    "🧮 Code Puzzle:\n"
                    "$ + $ + $ = 30\n"
                    "& + 2$ = 24\n"
                    "$ + & + @ = 20\n"
                    "@ x @ - 2$ = &&\n\n"
                    "&& - $ = Code"
                )
            elif game_state["dead_men_examined"] == 2:
                print("🧠 Hint: Each symbol represents a number.")
            elif game_state["dead_men_examined"] == 3:
                print("🧠 Hint: Start with the simplest equation.")
            else:
                print("🧠 Hint: Solve line by line.")

        if item_name == "picture" and key_e not in game_state["inventory"]:
            game_state["inventory"].append(key_e)
            print("🔑 You found a key.")

    #----------- ESCAPE ROOM ----------------
    if room["name"] == "escape room" and item_name == "door f":
        if safe_input("Enter final code: ") == "6":
            return "exit"
        else:
            print("That doesn’t seem right.")

    return None

#---------------- GAME LOOP ----------------------
def play_room(room):
    game_state["current_room"] = room
    print(f"\n📍 You are in the {room['name']}.")

    while True:
        action = safe_input("explore / examine / inventory / exit: ")

        if action == "explore":
            explore_room(room)

        elif action == "inventory":
            check_inventory()

        elif action == "examine":
            item = safe_input("Examine what: ")
            result = examine_item(item)

            if result == "exit":
                print("🎉 You escaped!")
                return

            if isinstance(result, dict):
                print(f"\n🔓 {item} unlocks.")
                print(f"➡️ You are now entering the {result['name']}.")
                play_room(result)
                return

        else:
            print("Invalid action.")

#---------------- START GAME -------------------------
print(
    "Hi You are about to start an escape room game!\n"
    "You wake up in a strange house.\n"
    "For each room you need to solve puzzles to find keys to unlock doors.\n"
    "Pay close attention to the descriptions and do your best!\n"
)

play_room(game_room)

import os
from colorama import Fore
import DataFuncs
import Points
import TTS
import time
import dupVerse

# ------------------- COLOR MAP -------------------
COLOR_MAP = {
    "FORE.BLACK": Fore.BLACK,
    "FORE.RED": Fore.RED,
    "FORE.GREEN": Fore.GREEN,
    "FORE.YELLOW": Fore.YELLOW,
    "FORE.BLUE": Fore.BLUE,
    "FORE.MAGENTA": Fore.MAGENTA,
    "FORE.CYAN": Fore.CYAN,
    "FORE.WHITE": Fore.WHITE
}

# ------------------- UTILITIES -------------------
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print("Invalid choice. Try again.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

# ------------------- HOME -------------------
def home() -> int:
    clear_terminal()
    print("Bible Verse Dictionary!")
    points = int(Points.get_points().decode('utf-8'))
    print(f"You have {points} Points")
    print("You can add your own Bible Verses for quick recall and memory practice!")
    print("|--------------------------------------------------|")
    print("| 1)Enter Groups 2)Make a Group 3)New Verse 4)Quit |")
    print("|--------------------------------------------------|")
    return get_int_input("Enter Choice Here: ") + 1

# ------------------- COLOR CHANGER -------------------
def color_changer(choice) -> str:
    return {
        1: Fore.LIGHTBLUE_EX,
        2: Fore.BLUE,
        3: Fore.GREEN,
        4: Fore.MAGENTA
    }.get(choice, Fore.RED)

# ------------------- NEW GROUP -------------------
def new_group(groups) -> int:
    print("Making a new group: Choose a name for the group and assign a color!")
    name = input("Group Name: ")
    print("|-------------------------------------------------|")
    print("| 1)Light Blue 2)Dark Blue 3)Green 4)Purple 5)Red |")
    print("|-------------------------------------------------|")
    color_choice = get_int_input("Enter Choice Here: ", 1, 5)
    color = color_changer(color_choice)
    groups.append([name, color, 0])
    return 1

# ------------------- INFO -------------------
def info_group_page():
    print("INFO:")
    print("This is where you can access all your groups. The Master List will have all your verses.")
    print("When you select a group you will have the following options (Study, Edit, Delete - cannot be undone)")
    input("Press ENTER to continue...")

# ------------------- DELETE GROUP -------------------
def delete_group(groups, choice):
    clear_terminal()
    if groups[choice][0] == "Master List":
        print(f"{Fore.RED}ATTENTION - YOU CANNOT DELETE THE MASTER LIST!{Fore.RESET}")
        input("Press ENTER to continue...")
        return
    print(f"{Fore.RED}ATTENTION - YOU CANNOT UNDO THIS ACTION!{Fore.RESET}")
    print("1)Continue 2)Back")
    option = get_int_input("Enter Choice Here: ", 1, 2)
    if option == 1:
        del groups[choice]

# ------------------- ADD VERSE -------------------
def add_verse(groups, verses_dict) -> int:
    print("|-------------------------|")
    print("| Choose a group for the new verse: |")
    for i, g in enumerate(groups):
        print(f"| {i}) {g[1]}{g[0]}{Fore.RESET}")
    print("|-------------------------|")

    choice = get_int_input("Enter group number: ", 0, len(groups)-1)
    group_name = groups[choice][0]

    reference = input("Verse Reference (e.g., John 3:16): ")
    text = input("Verse Text: ")

    if group_name not in verses_dict:
        verses_dict[group_name] = []
    verses_dict[group_name].append({"reference": reference, "text": text})

    for g in groups:
        if g[0] == group_name:
            g[2] += 1
            break

    print(f"Added verse to group '{group_name}'!")
    return 1

# ------------------- SED SCREEN -------------------
def SEDScreen(groups, choice, verses_dict) -> int:
    clear_terminal()
    print(f"What would you like to do with {groups[choice][1]}\"{groups[choice][0]}\"{Fore.RESET}?")
    print("|-------------------------|")
    print("| 1)Study 2)Delete 3)Back |")
    print("|-------------------------|")
    
    option = get_int_input("Enter your choice here: ", 1, 3)
    if option == 1:
        group_name = groups[choice][0]
        verses_list = verses_dict.get(group_name, [])
        study_page(group_name, verses_list, groups, verses_dict)
        return 2  # stay in group page
    elif option == 2:
        delete_group(groups, choice)
        return 2
    elif option == 3:  # back
        return 1  # go back to home page


# ------------------- MASTER LIST -------------------
def generate_master_list(groups, verses_dict):
    """
    Generates a deduplicated Master List for all groups.
    """
    all_verses = []
    for verse_list in verses_dict.values():
        all_verses.extend(verse_list)

    # Deduplicate using microservice
    all_verses = dupVerse.deduplicate_verses_by_reference(all_verses)

    master_group = ["Master List", Fore.GREEN, len(all_verses)]
    return master_group, all_verses



# ------------------- PRINT GROUP MENU -------------------
def print_groups_menu(groups, verses_dict):
    master_group, _ = generate_master_list(groups, verses_dict)
    print("|-------------------------|")
    print(f"| 0) {master_group[1]}{master_group[0]}{Fore.RESET} ({master_group[2]} verses)")
    for i, g in enumerate(groups):
        print(f"| {i+1}) {g[1]}{g[0]}{Fore.RESET} ({g[2]} verses)")
    base_index = len(groups) + 1
    print(f"| {base_index}) New Group            |")
    print(f"| {base_index+1}) Info                 |")
    print(f"| {base_index+2}) Back                 |")
    print("|-------------------------|")

# ------------------- GROUP PAGE -------------------
def group_page(groups, verses_dict) -> int:
    clear_terminal()
    print("Groups: Select which group to study/edit/delete")
    print_groups_menu(groups, verses_dict)

    choice = get_int_input("Enter Choice Here: ", 0, len(groups)+2)

    if choice == 0:  # Master List
        master_group, all_verses = generate_master_list(groups, verses_dict)
        study_page(master_group[0], all_verses, groups, verses_dict)
        return 2  # stay in groups page
    elif 1 <= choice <= len(groups):  # normal group
        return SEDScreen(groups, choice-1, verses_dict)
    elif choice == len(groups)+1:  # New Group
        new_group(groups)
        return 2
    elif choice == len(groups)+2:  # Back
        return 1  # go back to home page

# ------------------- JSON <-> ARRAYS -------------------
def json_to_arrays(user_data):
    groups_array = []
    verses_dict = {}
    for group_name, group_info in user_data.get("groups", {}).items():
        color_str = group_info.get("color", "FORE.WHITE")
        color_obj = COLOR_MAP.get(color_str, Fore.WHITE)
        verses = group_info.get("verses", [])
        groups_array.append([group_name, color_obj, len(verses)])
        verses_dict[group_name] = verses
    return groups_array, verses_dict

def arrays_to_json(user_id, groups_array, verses_dict):
    groups_json = {}
    for group_name, color_obj, _ in groups_array:
        color_str = next((k for k, v in COLOR_MAP.items() if v == color_obj), "FORE.WHITE")
        verse_list = verses_dict.get(group_name, [])
        groups_json[group_name] = {"color": color_str, "verses": verse_list}
    return {"user_id": user_id, "groups": groups_json}

# ------------------- STUDY PAGE -------------------
def study_page(group_name, verses_list, groups, verses_dict):
    while True:
        clear_terminal()
        print(f"Studying Group: {group_name} ({len(verses_list)} verses)")
        print("|---------------------------|")
        print("| 1) Listen to Verses       |")
        print("| 2) Type the Verses        |")
        print("| 3) Back                   |")
        print("|---------------------------|")

        choice = input("Enter your choice: ")
        if choice == "1":
            listen_verses(verses_list)
            input("Finished listening. Press ENTER to continue...")
        elif choice == "2":
            type_verses(verses_list)
        elif choice == "3":
            return 1
        else:
            print("Invalid choice. Try again.")
            input("Press ENTER to continue...")

def listen_verses(verses_list):
    for v in verses_list:
        clear_terminal()
        print(f"Listening to: {v['reference']}")
        print(v['text'])
        TTS.create_and_play(f"{v['reference']}: {v['text']}")
        time.sleep(0.3)

def type_verses(verses_list):
    for v in verses_list:
        clear_terminal()
        print(f"Verse Reference: {v['reference']}")
        print("Type the verse below:")
        user_input = input("> ")
        if user_input.strip() == v['text'].strip():
            print(f"{Fore.GREEN}Correct!{Fore.RESET}")
            points = int(Points.add_points(5).decode('utf-8'))
            print(f"You now have {points} Points!")
        else:
            print(f"{Fore.RED}Incorrect!{Fore.RESET}")
            print(f"Correct verse: {v['text']}")
        input("Press ENTER for next verse...")

# ------------------- MAIN -------------------
def main():
    data = DataFuncs.getData()
    groups, verses = json_to_arrays(data)
    page = 1

    while True:
        if page == 1:  # HOME
            page = home()
        elif page == 2:  # GROUP PAGE
            page = group_page(groups, verses)
        elif page == 3:  # NEW GROUP
            page = new_group(groups)
        elif page == 4:  # NEW VERSE
            page = add_verse(groups, verses)
        elif page == 5:  # QUIT
            data = arrays_to_json("user_001", groups, verses)
            DataFuncs.pushData(data)
            clear_terminal()
            break

if __name__ == "__main__":
    main()

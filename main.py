import os
from colorama import Fore

class textcolors:
    NEW = '\033[0m'
    RED = '\033[31m'
    LIGHTBLUE = ''
    DARKBLUE = ''
    GREEN = '\033[32m'
    PURPLE = ''
def clear_terminal():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For Unix-like systems (Linux, macOS)
        _ = os.system('clear')
def home() -> int:
    print("Bible Verse Dictionary!\n")
    print("You can Add your own Bible Verses for quick recall and memory practice!")
    print("|--------------------------------------|")
    print("| 1)Enter Groups 2)Make a Group 3)Quit |")
    print("|--------------------------------------|")
    choice = input("Enter Choice Here: ")
    return int(choice) + 1

def color_changer(color) -> str:
    if color == 1:
        return Fore.LIGHTBLUE_EX
    elif color == 2:
        return Fore.BLUE
    elif color == 3:
        return Fore.GREEN
    elif color == 4:
        return Fore.MAGENTA
    else:
        return Fore.RED
    
def new_group(group) -> int:
    print("Making a new group: Choose a name for the group and assign a color for better memory!(you can edit this later)")
    name = input("Group Name: ") 
    print("|-------------------------------------------------|")
    print("| 1)Light Blue 2)Dark Blue 3)Green 4)Purple 5)Red |")
    print("|-------------------------------------------------|")
    color = input("Enter Choice Here: ")

    color = color_changer(int(color))

    group.append([name, color, 0])
    return 1

def info_group_page():
    print("INFO:")
    print("This is where you can access all your groups. The Master List will have all your verses. On this screen you can select a group or make a new group.")
    print("When you select a group you will have the following options (Study, Edit, Delete - this action cannot be undone)")
    input("Press \"ENTER\" to continue...")

def delete_group(group, choice):
    clear_terminal()
    if group[choice][0] == "Master List":
        print(f"{Fore.RED}ATTENTION - YOU CANNOT DELETE THE MASTER LIST!{Fore.RESET}")
        input("Press \"ENTER\" to continue...")

        return
    print(f"{Fore.RED}ATTENTION - YOU CANNOT UNDO THIS ACTION!{Fore.RESET}")
    print("1)Continue 2)Back")
    option = input("Enter Choice Here: ")
    option = int(option)
    if option == 1:
        del group[choice]

def SEDScreen(group, choice) -> int:
    clear_terminal()
    print(f"What would you like to do with {group[choice][1]}\"{group[choice][0]}\"{Fore.RESET}?")
    print("|--------------------------------|")
    print("| 1)Study 2)Edit 3)Delete 4)Back |")
    print("|--------------------------------|")
    
    option = input("Enter your choice here: ")
    option = int(option)
    if option == 1:
        clear_terminal()
        print("Sorry you cannot study yet!")
        input("Press \"ENTER\" to continue...")
        return 2
    elif option == 2:
        clear_terminal()
        print("Sorry you cannot Edit yet!")
        input("Press \"ENTER\" to continue...")
        return 2
    elif option == 3:
        delete_group(group, choice)
        return 2
    else:
        return 2
        


def group_page(group) -> int:
    print("Groups: Select which group then if you want to study/edit/delete")
    print("|-------------------------|")
    for i in range(len(group)):
        print(f"| {i}) {group[i][1]}{group[i][0]}",Fore.RESET)
    print(f"| {len(group)}) New Group            |")
    print(f"| {len(group)+1}) info                 |")
    print(f"| {len(group)+2}) Back                 |")
    print("|-------------------------|")

    choice = input("Enter Choice Here: ")
    choice = int(choice)
    if choice < len(group):
        return SEDScreen(group, choice)
    elif choice == len(group):
        return 3
    elif choice == len(group)+1:
        clear_terminal()
        info_group_page()
        return 2
    else:
        return 1




page = 1
group = [["Master List", Fore.GREEN, 2]]
while True:
    if page == 1: #HOME
        clear_terminal() 
        page = home()

    elif page == 2:#Group Page
        clear_terminal()
        page = group_page(group)

    elif page == 3 :#Create a New Group
        clear_terminal() 
        page = new_group(group)

    elif page == 4:#Quit --Todo: create a saving feature
        clear_terminal()
        break
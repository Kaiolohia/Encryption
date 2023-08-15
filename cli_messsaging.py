import messaging
import time
from os import system

running = True
u = messaging.User()

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def formatMessages(m:list):
    for i in reversed(m):
        print(f"{i['author']}: {i['message']}")
    print("\n\n")

#Group loop
def inGroup():
    inGroup = True
    while inGroup:
        clear()
        formatMessages(u.getMessages())
        message = input("Type your messsage here\nType --back to exit group\n-> ")
        if "--back" in message:
            inGroup = False
            return
        u.sendMessage(message)

# Main loop
while running:
    if not u.isLoggedIn():
        print("Welcome to encrypted messaging!")
        u_action = input("Login or Register?\n-> ").lower()
        if u_action == "login":
            attempting_login = True
            while attempting_login:
                name = input("Please enter your username\n-> ")
                password = input("Please enter your password\n-> ")
                try:
                    u.login(name, password)
                except Exception as e:
                    print(e)
                    retry = input("Would you like to try to sign in again? Y/N\n-> ").lower()
                    if retry == "n":
                        attempting_login = False
                if u.isLoggedIn():
                    attempting_login = False
        elif u_action == "register":
            name = input("Please enter your username\n-> ")
            password = input("Please enter your password\n-> ")
            u.register(name, password)
        else:
            print("\n\n\n**Invalid action**\n\n\n")
            time.sleep(2)
    else:
        print(f"Welcome {u.username}!")
        print(f"You have {len(u.groups)} groups avalible:")
        for g in u.groups:
            print(f"   - {g}")
        u_action = input("Would you like to create a group or select a group? C/S\nType --logout to logout\n-> ").lower()
        if u_action == "s":
            u.selectGroup(int(input(f"Select a group number.\n-> ")))
            inGroup()
        elif u_action == "c":
            print("Create a group!")
            print(f"Avalible users:")
            for i in range(len(messaging.pj.users)-1):
                if i != int(u.uid):
                    print(messaging.pj.users[str(i)]["name"])

            s_users = messaging.pj.getIDbyUsernames(input("Select a user to make a group with\nTo make a group with multible users, Type their name followed by a comma and a space\nex: \"Bob, Joe\"\n-> ").split(", "))
            u.createGroup(s_users)
            inGroup()
        elif u_action == "--logout":
            u.logout()
            clear()
        else:
            clear()
            print("Invalid input, please try again!")
            time.sleep(2)
            clear()
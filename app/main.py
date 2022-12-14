import os
import sys
import time
import mysql.connector
from mysql.connector import Error
from termcolor import colored, cprint
from secrets import host, database, user, password

# Testing BD Connection
def test_connection(connection):
    if connection.is_connected():
        db_Info = connection.get_server_info()
        cprint(f"Connected to MySQL Server version {db_Info}", attrs=["dark"])
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        cprint(f"You're connected to database: {record}", attrs=["dark"])
        cursor.close()


LOGO = """
 ____                                     _
|  _ \ __ _ ___ _____      _____  _ __ __| |
| |_) / _` / __/ __\ \ /\ / / _ \| '__/ _` |
|  __/ (_| \__ \__ \\\ V  V / (_) | | | (_| |
|_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|

 __  __
|  \/  | __ _ _ __   __ _  __ _  ___ _ __
| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
| |  | | (_| | | | | (_| | (_| |  __/ |
|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|
                          |___/

Docker, Python & MySQL


"""

OPTIONS = """1. Add a new credential
2. Find an existing credential
3. Update a credential 
4. Delete a credential
5. List all credentials
0. Exit program
"""

QUERY_OPTIONS = """1. URL
2. Username
"""


# 1. Add new password
def add_credential(connection):
    print("\n\n")
    cprint("-" * 30, "blue")
    cprint("INSERT THE CREDENTIAL", "blue")
    cprint("-" * 30, "blue")
    url = input("+ URL: ").strip()
    user = input("+ Username: ").strip()
    password = input("+ Password: ").strip()
    command = f'INSERT INTO secrets(url, user, password) VALUES("{url}", "{user}", "{password}")'
    cursor = connection.cursor()
    cursor.execute(command)
    cursor.close()
    connection.commit()


# 2. Find an existing password
def find_credential(connection, res):
    if res == "url":
        to_search = input("* URL -> ").strip()
    elif res == "user":
        to_search = input("* Username -> ").strip()
    command = f'select * from secrets where {res} = "{to_search}"'
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    return result


# 3. Update an existing password
def update_credential(connection, res):
    if res == "url":
        to_search = input("* URL -> ").strip()
    elif res == "user":
        to_search = input("* Username -> ").strip()
        
    new_value_url = input("+ New value (URL) -> ").strip()
    new_value_user = input("+ New value (Username) -> ").strip()
    new_value_pass = input("+ New value (Password) -> ").strip()

    opt2 = input(
        f"\n\n{query_count(connection, res, to_search)} item will be updated, are you sure? [Y/n] ").strip().lower()

    command = f'update secrets set url = "{new_value_url}", user ="{new_value_user}", password ="{new_value_pass}" where {res} = "{to_search}"'
    cursor = connection.cursor()
    cursor.execute(command)
    cursor.close()
    
    if opt2 == "y":
        connection.commit()
    else:
        connection.rollback()


# 4. Delete a password
def delete_credential(connection, res):
    if res == "url":
        to_search = input("* URL -> ").strip()        
    elif res == "user":
        to_search = input("* Username -> ").strip()
    
    opt2 = input(
        f"\n\n{query_count(connection, res, to_search)} item will be deleted, are you sure? [Y/n] ").strip().lower()
    
    command = f'delete from secrets where {res} = "{to_search}"'
    cursor = connection.cursor()
    cursor.execute(command)
    cursor.close()
    
    if opt2 == "y":
        connection.commit()
    else:
        connection.rollback()


# 5. List all passwords
def show_all_credentials(connection):
    command = f'select * from secrets'
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    format_to_command_line(result)


#####################################
# Aux functions
#####################################
def query_count(connection, res, to_search):
    command = f'select * from secrets where {res} = "{to_search}"'
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    return len(result)


def format_to_command_line(result):
    print("\n")
    cprint("-" * 30, "blue")
    cprint(f"YOU HAVE {len(result)} CREDENTIAL", "blue")
    cprint("-" * 30, "blue")
    for index, item in enumerate(result):
        cprint(f"\nITEM {index + 1}", "green")
        cprint("-" * 30, "green")
        print(f"URL = {item[1]}\nUsername = {item[2]}\nPassword = {item[3]}")


def query_menu():
    print("\n")
    cprint("-" * 30, "blue")
    cprint("QUERY CREDENTIAL BY ...", "blue")
    cprint("-" * 30, "blue")
    print(QUERY_OPTIONS)
    opt = input(": ").strip()
    if opt.isnumeric():
        opt = int(opt)
        if opt == 1:
            return "url"
        elif opt == 2:
            return "user"
        else:
            cprint("\n[!] Invalid option, choose between 1 and 2!",
                   "red", attrs=["bold"], file=sys.stderr)
    else:
        cprint("\n[!] Invalid option, please insert only a number!",
               "red", attrs=["bold"], file=sys.stderr)


#####################################
# Main
#####################################
def main(connection):

    while True:
        os.system("clear")
        test_connection(connection)
        cprint(LOGO, "green", attrs=["bold"], file=sys.stderr)
        cprint("CHOOSE AN OPTION\n")
        cprint(OPTIONS)

        opt = input(": ").strip()
        if opt.isnumeric():
            opt = int(opt)
            if opt == 0:
                cprint("\n\nThank you by coming! :)\n\n", "yellow")
                exit()
            elif opt == 1:  # Create
                add_credential(connection)
                input(colored("\n\nPress enter to return to the previous menu\n", attrs=["dark"]))
            elif opt == 2:  # Read
                res = 0
                while res not in ("url", "user"):
                    res = query_menu()
                result = find_credential(connection, res)
                format_to_command_line(result)
                input(colored("\n\nPress enter to return to the previous menu\n", attrs=["dark"]))
            elif opt == 3:  # Update
                res = 0
                while res not in ("url", "user"):
                    res = query_menu()
                update_credential(connection, res)
                input(colored("\n\nPress enter to return to the previous menu\n", attrs=["dark"]))
            elif opt == 4:  # Delete
                res = 0
                while res not in ("url", "user"):
                    res = query_menu()
                delete_credential(connection, res)
                input(colored("\n\nPress enter to return to the previous menu\n", attrs=["dark"]))
            elif opt == 5:  # Read all
                show_all_credentials(connection)
                input(colored("\n\nPress enter to return to the previous menu\n", attrs=["dark"]))
            else:
                cprint("\n[!] Invalid option, choose between 0 and 5!",
                       "red", attrs=["bold"], file=sys.stderr)
                time.sleep(3)
        else:
            cprint("\n[!] Invalid option, please insert only a number!",
                   "red", attrs=["bold"], file=sys.stderr)
            time.sleep(3)


#####################################
# Authentication
#####################################
def authentication(connection):
    command = f'select * from auth'
    cursor = connection.cursor()
    cursor.execute(command)
    response = cursor.fetchone()
    cursor.close()

    # [1] = `status` -> 0 = first login, 1 = already setted
    print(response[1])
    if response[1] == 0:
        os.system("clear")
        test_connection(connection)
        cprint(LOGO, "green", attrs=["bold"], file=sys.stderr)
        master_password = input(colored("[!] SET A MASTER PASSWORD: ", "yellow")).strip()

        com = f'update auth set status = 1, master_password = "{master_password}"'
        cursor = connection.cursor()
        cursor.execute(com)
        cursor.close()
        connection.commit()

    elif response[1] == 1:
        while True:
            os.system("clear")
            test_connection(connection)
            cprint(LOGO, "green", attrs=["bold"], file=sys.stderr)
            master_password = input(colored("[!] MASTER PASSWORD: ", "yellow")).strip()

            com = f'select * from auth where master_password = "{master_password}"'
            cursor = connection.cursor()
            cursor.execute(com)
            result = cursor.fetchone()
            cursor.close()

            if result is None:
                cprint(f"\n[!] Incorrect password, please try again!",
                       "red", attrs=["bold"], file=sys.stderr)
                time.sleep(2)
            else:
                cprint(f"\n[!] Correct password! :)",
                       "green", attrs=["bold"], file=sys.stderr)
                time.sleep(2)
                break


# Start
if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        
        authentication(connection)
        main(connection)

        if connection.is_connected():
            connection.close()

    except KeyboardInterrupt as ki:
        cprint("\n\nThank you by coming! :)\n\n", "yellow")
        exit()

    except Error as e:
        cprint(f"[!] Error while connecting to MySQL\n[!] {e}",
               "red", attrs=["bold"], file=sys.stderr)

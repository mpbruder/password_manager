import os
import mysql.connector
from mysql.connector import Error

# Testing BD Connection
def test_connection(connection):
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
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

OPTIONS = """CHOOSE AN OPTION
1. Add a new credential
2. Find an existing credential
3. Update a credential 
4. Delete a credential
5. List all credentials
0. Exit program
"""

QUERY_OPTIONS = """1. Url
2. Username / email
"""


# 1. Add new password
def add_credential(connection):
    print("\n\n")
    print("-" * 30)
    print("INSERT THE CREDENTIAL")
    print("-" * 30)
    url = input("URL: ").strip()
    user = input("Username / email: ").strip()
    password = input("Password: ").strip()
    command = f'INSERT INTO secrets(url, user, password) VALUES("{url}", "{user}", "{password}")'
    cursor = connection.cursor()
    cursor.execute(command)
    cursor.close()
    connection.commit()


# 2. Find an existing password
def find_credential(connection, res):
    if res == "url":
        url = input(": URL -> ").strip()
        command = f'select * from secrets where url = "{url}"'
    elif res == "user":
        user = input(": User/email -> ").strip()
        command = f'select * from secrets where user = "{user}"'
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    return result


# 3. Update an existing password
def update_credential(connection, res):
    if res == "url":
        url = input(": URL -> ").strip()
        new_value_url = input(": New value (url) -> ").strip()
        new_value_user = input(": New value (user) -> ").strip()
        new_value_pass = input(": New value (password) -> ").strip()
        command = f'update secrets set url = "{new_value_url}", user ="{new_value_user}", password ="{new_value_pass}" where url = "{url}"'
        opt2 = input(
            f"\n\n{len(query_count(connection, res, url))} item will be updated, are you sure? [Y/n] ").strip().lower()
    elif res == "user":
        user = input(": User/email -> ").strip()
        new_value = input(": New value -> ").strip()
        command = f'update secrets set url = "{new_value_url}", user ="{new_value_user}", password ="{new_value_pass}" where user = "{user}"'
        opt2 = input(
            f"\n\n{len(query_count(connection, res, user))} item will be updated, are you sure? [Y/n] ").strip().lower()
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
        url = input(": URL -> ").strip()
        command = f'delete from secrets where url = "{url}"'
        opt2 = input(
            f"\n\n{len(query_count(connection, res, url))} item will be deleted, are you sure? [Y/n] ").strip().lower()
    elif res == "user":
        user = input(": User/email -> ").strip()
        command = f'delete from secrets where user = "{user}"'
        opt2 = input(
            f"\n\n{len(query_count(connection, res, user))} item will be deleted, are you sure? [Y/n] ").strip().lower()
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
def query_count(connection, res, type):
    command = f'select * from secrets where {res} = "{type}"'
    cursor = connection.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    cursor.close()
    return result


def format_to_command_line(result):
    print("-" * 30)
    print(f"YOUR {len(result)} CREDENTIALS")
    print("-" * 30)
    for index, item in enumerate(result):
        print(f"\nITEM {index + 1}")
        print("-" * 30)
        print(f"Url = {item[1]}\nUser = {item[2]}\nPassword = {item[3]}")


def query_menu():
    print("\n")
    print("-" * 30)
    print("QUERY CREDENTIAL BY ...")
    print("-" * 30)
    print(QUERY_OPTIONS)
    opt = int(input(": "))
    if opt == 1:
        return "url"
    elif opt == 2:
        return "user"
    else:
        print("Invalid option, try another one!")


#####################################
# Main
#####################################
def main(connection):

    while True:
        os.system("clear")
        test_connection(connection)
        print("\n")
        print(LOGO)
        print(OPTIONS)

        opt = int(input(": "))
        if opt == 0:
            print("\n\nThank you by coming! :)\n\n")
            exit()
        elif opt == 1:  # Create
            add_credential(connection)
            input("\n\nPress enter to return to the previous menu\n")
        elif opt == 2:  # Read
            res = query_menu()
            result = find_credential(connection, res)
            format_to_command_line(result)
            input("\n\nPress enter to return to the previous menu\n")
        elif opt == 3:  # Update
            res = query_menu()
            update_credential(connection, res)
            input("\n\nPress enter to return to the previous menu\n")
        elif opt == 4:  # Delete
            res = query_menu()
            delete_credential(connection, res)
            input("\n\nPress enter to return to the previous menu\n")
        elif opt == 5:  # Read all
            show_all_credentials(connection)
            input("\n\nPress enter to return to the previous menu\n")
        else:
            print("Invalid option, try another one!")


if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='secrets_db',
                                             user='mpbruder',
                                             password='0123')
        main(connection)

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            connection.close()

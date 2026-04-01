import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE
    )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute(
                """
                INSERT INTO contacts (first_name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING
                """,
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()

def insert_from_console():
    name = input("NAME: ")
    phone = input("PHONE: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

def update_contact():
    phone = input("PHONE: ")
    new_name = input("New name (Enter if not needed): ")
    new_phone = input("New phone (Enter if not needed): ")
    conn = get_connection()
    cur = conn.cursor()
    if new_name:
        cur.execute(
            "UPDATE contacts SET first_name = %s WHERE phone = %s",
            (new_name, phone)
        )
    if new_phone:
        cur.execute(
            "UPDATE contacts SET phone = %s WHERE phone = %s",
            (new_phone, phone)
        )
    conn.commit()
    cur.close()
    conn.close()

def search_contacts():
    keyword = input("Enter name or phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM contacts
        WHERE first_name ILIKE %s OR phone LIKE %s
        """,
        (f"%{keyword}%", f"{keyword}%")
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter name or phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM contacts WHERE first_name = %s OR phone = %s",
        (value, value)
    )
    conn.commit()
    cur.close()
    conn.close()

def menu():
    create_table()

    while True:
        print("\n--- PHONEBOOK ---")
        print("1 - Import CSV")
        print("2 - Add contact")
        print("3 - Update contact")
        print("4 - Search")
        print("5 - Delete")
        print("0 - Exit")

        choice = input("Choice: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Error")


if __name__ == "__main__":
    menu()
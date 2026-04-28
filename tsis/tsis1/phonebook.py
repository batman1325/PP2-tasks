"""
PhoneBook — TSIS 1
"""

import psycopg2
import csv
import json
from config import load_config


def get_conn():
    return psycopg2.connect(**load_config())


def print_row(r):
    cid, name, email, bday, grp, phones = r
    print(f"  [{cid}] {name} | email: {email or '-'} | bday: {bday or '-'} | "
          f"group: {grp or '-'} | phones: {phones or '-'}")

# DB HELPERS

def db_call(proc, params, fetch=False):
    """Call stored procedure or function"""
    try:
        with get_conn() as conn, conn.cursor() as cur:
            sql = f"SELECT * FROM {proc}({','.join(['%s']*len(params))})" if fetch else \
                  f"CALL {proc}({','.join(['%s']*len(params))})"
            cur.execute(sql, params)
            if fetch:
                return cur.fetchall()
            conn.commit()
            for n in conn.notices:
                print(n.strip())
    except Exception as e:
        print(f"Error: {e}")


def db_exec(sql, params=None, fetch=False):
    """Execute any SQL query"""
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, params or ())
            if fetch:
                return cur.fetchall()
            conn.commit()
            return cur.rowcount
    except Exception as e:
        print(f"Error: {e}")
        return 0


# MAIN FUNCTIONS

def check_setup():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name IN ('phonebook','phones','groups')")
            tables = {r[0] for r in cur.fetchall()}
            cur.execute("SELECT routine_name FROM information_schema.routines WHERE routine_schema='public' AND routine_name IN ('upsert_u','loophz','del_user','add_phone','move_to_group','pagination','search_contacts')")
            routines = {r[0] for r in cur.fetchall()}

        if all(t in tables for t in ['groups','phonebook','phones']) and all(r in routines for r in ['upsert_u','loophz','del_user','add_phone','move_to_group','pagination','search_contacts']):
            print("OK — Database is ready.")
        else:
            print("Some tables or procedures are missing. Run setup.sql in psql.")
    except Exception as e:
        print(f"Connection error: {e}")


def upsert_contact():
    u = input("Username: ").strip()
    p = input("Phone: ").strip()
    t = input("Type [mobile]: ").strip() or "mobile"
    db_call("upsert_u", (u, p, t))
    print(f"Done — '{u}' saved.")


def bulk_insert():
    users = input("Usernames (space sep): ").split()
    phones = input("Phones (same order): ").split()
    if len(users) != len(phones):
        print("Count mismatch.")
        return
    db_call("loophz", (users, phones))
    print("Bulk insert completed.")


def update_contact():
    print("1.Name  2.Email  3.Birthday")
    field = {"1":"username","2":"email","3":"birthday"}.get(input("Choice: ").strip())
    if not field: return print("Invalid.")
    old = input("Current username: ").strip()
    new = input(f"New {field}: ").strip()
    changed = db_exec(f"UPDATE phonebook SET {field}=%s WHERE username=%s", (new, old))
    print("Updated." if changed else "Not found.")


def add_phone():
    db_call("add_phone", (input("Username: ").strip(), 
                          input("Phone: ").strip(), 
                          input("Type [mobile]: ").strip() or "mobile"))


def move_to_group():
    db_call("move_to_group", (input("Username: ").strip(), input("Group: ").strip()))


def query_contacts():
    print("Filter: 1.Name  2.Phone  3.Email")
    mode = input("Choice: ").strip()
    print("Sort: 1.Name  2.Birthday  3.Date")
    sort = {"1":"c.username","2":"c.birthday","3":"c.created_at"}.get(input("Choice: ").strip(), "c.username")

    where_map = {"1": ("c.username ILIKE %s", lambda x: f"%{x}%"),
                 "2": ("p.phone LIKE %s",     lambda x: f"{x}%"),
                 "3": ("c.email ILIKE %s",    lambda x: f"%{x}%")}

    if mode not in where_map: return print("Invalid.")
    where, trans = where_map[mode]
    val = trans(input("Value: ").strip())

    sql = f"""
        SELECT c.id, c.username, c.email, c.birthday, g.name,
               STRING_AGG(p.phone||' ('||COALESCE(p.type,'?')||')', ', ')
        FROM phonebook c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE {where}
        GROUP BY c.id, c.username, c.email, c.birthday, g.name, c.created_at
        ORDER BY {sort}
    """
    rows = db_exec(sql, (val,), fetch=True)
    [print_row(r) for r in rows] if rows else print("No results.")


def filter_by_group():
    groups = db_exec("SELECT id, name FROM groups ORDER BY name", fetch=True)
    print("Groups:")
    for gid, name in groups:
        print(f"  {gid}. {name}")

    choice = input("Group name or ID: ").strip()
    col = "g.id" if choice.isdigit() else "g.name"
    val = int(choice) if choice.isdigit() else choice

    sql = f"""
        SELECT c.id, c.username, c.email, c.birthday, g.name,
               STRING_AGG(p.phone||' ('||COALESCE(p.type,'?')||')', ', ')
        FROM phonebook c JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE {col} = %s
        GROUP BY c.id, c.username, c.email, c.birthday, g.name
        ORDER BY c.username
    """
    rows = db_exec(sql, (val,), fetch=True)
    [print_row(r) for r in rows] if rows else print("No contacts in group.")


def full_search():
    q = input("Search: ").strip()
    rows = db_call("search_contacts", (q,), fetch=True) or []
    [print_row(r) for r in rows] if rows else print("No results.")


def paginated_browse():
    size, page = 5, 0
    while True:
        rows = db_call("pagination", (size, page * size), fetch=True) or []
        if not rows and page == 0:
            return print("No contacts.")

        print(f"\n--- Page {page + 1} ---")
        for r in rows: print_row(r)
        if len(rows) < size: print("(last page)")

        cmd = input("next/prev/quit: ").strip().lower()
        if cmd == "next": page += 1 if len(rows) == size else 0
        elif cmd == "prev": page = max(0, page - 1)
        elif cmd == "quit": break


def delete_contact():
    print("1.Username  2.Phone")
    choice = input("Choice: ").strip()
    if choice not in ("1", "2"): return print("Invalid.")
    val = input("Value: ").strip()
    db_call("del_user", (val,))
    print("Deleted.")


def csv_import():
    path = input("CSV path [contacts.csv]: ").strip() or "contacts.csv"
    try:
        with open(path, newline='', encoding='utf-8') as f:
            data = list(csv.DictReader(f))
    except FileNotFoundError:
        return print("File not found.")

    inserted = skipped = 0
    with get_conn() as conn, conn.cursor() as cur:
        for row in data:
            username = row.get('username', '').strip()
            if not username:
                skipped += 1
                continue
            # Simple insert logic (can be extended)
            cur.execute("INSERT INTO phonebook (username) VALUES (%s) ON CONFLICT DO NOTHING", (username,))
            if cur.rowcount > 0:
                inserted += 1
    print(f"CSV import done: {inserted} inserted, {skipped} skipped.")


def export_json():
    path = input("Output [contacts.json]: ").strip() or "contacts.json"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, username, email, birthday::text, (SELECT name FROM groups WHERE id = group_id) FROM phonebook ORDER BY username")
        data = []
        for cid, name, email, bday, group in cur.fetchall():
            cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (cid,))
            phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]
            data.append({"username": name, "email": email, "birthday": bday, "group": group, "phones": phones})

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(data)} contacts.")


def import_json():
    path = input("JSON file [contacts.json]: ").strip() or "contacts.json"
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return print(f"JSON error: {e}")

    print(f"Imported {len(data)} contacts (simplified version).")


# MENU

def main():
    menu = {
        1: check_setup, 2: upsert_contact, 3: bulk_insert, 4: update_contact,
        5: add_phone, 6: move_to_group, 7: query_contacts, 8: filter_by_group,
        9: full_search, 10: paginated_browse, 11: delete_contact,
        12: csv_import, 13: export_json, 14: import_json
    }

    while True:
        print("""
PhoneBook — TSIS 1
----------------------------------
 1.Check   2.Upsert   3.Bulk   4.Update   5.Add Phone
 6.Group   7.Query   8.Filter  9.Search  10.Browse
11.Delete 12.CSV     13.JSON   14.Import  0.Exit
----------------------------------""")
        try:
            ch = int(input("Choice: ").strip())
            if ch == 0:
                print("Goodbye!")
                break
            menu.get(ch, lambda: print("Unknown option."))()
        except ValueError:
            print("Enter a number.")


if __name__ == "__main__":
    main()
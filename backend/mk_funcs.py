# import psycopg2
from backend import connection


def get_all_mk():
    con = connection.__get_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM master_key')
    return cur.fetchall()


def has_mk(mk):
    con = connection.__get_connection()
    cur = con.cursor()
    cur.execute('SELECT EXISTS(SELECT id FROM master_key WHERE encrypted_control_string = (%s))', (mk,))
    result = cur.fetchone()[0]
    cur.close()
    con.close()
    return result

    
def add_new_mk(mk):
    con = connection.__get_connection()
    cur = con.cursor()
    cur.execute('INSERT INTO master_key (encrypted_control_string) VALUES (%s)', (mk,))
    con.commit()
        
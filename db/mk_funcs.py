import psycopg2
from backend import connection

def is_mk(mk):
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
    try:
        cur.execute('INSERT INTO master_key (encrypted_control_string) VALUES (%s)', (mk,))
        con.commit()
        return True
    except psycopg2.Error:
        return False
    finally:
        cur.close()
        con.close()
        
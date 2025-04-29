import psycopg2
from backend import connection
from backend.encrypting.encrypting_mk import encrypting_mk

def is_mk(mk):
    con = connection.__get_connection()
    cur = con.cursor()
    cur.execute('SELECT encrypted_control_string, salt FROM master_key WHERE id = 1') #это в случае если у нас одна запись в мастеркей, иначе нужно будет брать во внимание айдишник 
    db_mk, db_salt = cur.fetchone()
    if (db_mk, db_salt):
        entered_mk_encr, _ = encrypting_mk(mk, db_salt)
        cur.close()
        con.close()
        return db_mk == entered_mk_encr
    cur.close()
    con.close()
    return False

    
def add_new_mk(mk):
    con = connection.__get_connection()
    cur = con.cursor()
    encrypted_control_string, salt = encrypting_mk(mk)
    try:
        cur.execute('INSERT INTO master_key (encrypted_control_string, salt) VALUES (%s, %s)', (encrypted_control_string, salt))
        con.commit()
        return True
    except psycopg2.Error:
        return False
    finally:
        cur.close()
        con.close()
        
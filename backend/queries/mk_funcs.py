import psycopg2

from backend import connection
from backend.encrypting.decrypt import decrypt
from backend.encrypting.encrypt import encrypt


def is_mk(mk):
    con = connection.__get_connection()
    cur = con.cursor()
    cur.execute('''SELECT encrypted_control_string, salt 
                FROM master_key WHERE id = 1''')  
    # потом будет (...WHERE login = %s),(login,) 
    # и логин пердается в is_mk что ли
    encrypted_value, salt = cur.fetchone()
    encrypted_value = encrypted_value.tobytes()
    salt = salt.tobytes()
    try:
        decrypt(mk, encrypted_value, salt)
    except Exception:
        return False
    finally:
        cur.close()
        con.close()
    return True

    
def add_new_mk(mk):
    con = connection.__get_connection()
    cur = con.cursor()
    encrypted_control_string, salt = encrypt(mk)
    try:
        cur.execute('''INSERT INTO master_key 
                    (encrypted_control_string, salt)
                    VALUES (%s, %s)''', (encrypted_control_string, salt))
        con.commit()
        return True
    except psycopg2.Error:
        return False
    finally:
        cur.close()
        con.close()
        
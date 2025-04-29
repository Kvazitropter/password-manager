import psycopg2


def __get_connection():
    con = psycopg2.connect(
        port=5432,
        host='localhost',
        database='password_manager',
        user='postgres',
        password='xxXX1234'
    )
    
    return con


def get_accounts():
    con = __get_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM account_details')
    return cur.fetchall()
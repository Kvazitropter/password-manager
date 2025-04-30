import psycopg2


class Repository:
    def get_connection(self):
        connection = psycopg2.connect(
            port=5432,
            host='localhost',
            database='password_manager',
            user='postgres',
            password='xxXX1234'
        )
        
        return connection
    
    
    def close_connection(self, connection, cur):
        connection.close()
        cur.close()


    def has_login_query(self, login):
        con = self.get_connection()
        cur = con.cursor()
        
        cur.execute(
            'SELECT EXISTS(SELECT 1 FROM master_key WHERE login = (%s))',
            (login,)
        )
        result = cur.fetchone()[0]

        self.close_connection(con, cur)
        return result


    def get_memory_mk_and_salt_query(self, login):
        con = self.get_connection()
        cur = con.cursor()

        cur.execute(
            'SELECT salt, encrypted_control_string FROM master_key WHERE login = %s',
            (login,)
        )
        result = cur.fetchone()

        self.close_connection(con, cur)
        return result


    def add_new_account_query(self, login, encrypted_control_string, salt):
        con = self.get_connection()
        cur = con.cursor()

        cur.execute(
            'INSERT INTO master_key (login, encrypted_control_string, salt) VALUES (%s, %s, %s)',
            (login, encrypted_control_string, salt)
        )
        con.commit()

        self.close_connection(con, cur)
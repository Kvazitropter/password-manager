import psycopg2

from backend.custom_errors import ConnectionError


class Repository:
    def __get_connection(self):
        try:
            connection = psycopg2.connect(
                port=5432,
                host='localhost',
                database='password_manager',
                user='postgres',
                password='xxXX1234'
            )

            return connection
        except psycopg2.OperationalError:
            raise ConnectionError

    def __close_connection(self, connection, cur):
        connection.close()
        cur.close()

    def has_account_query(self, login):
        con = self.__get_connection()
        cur = con.cursor()

        cur.execute(
            'SELECT EXISTS(SELECT 1 FROM "user" WHERE login = (%s))',
            (login,)
        )
        result = cur.fetchone()[0]

        self.__close_connection(con, cur)
        return result

    def get_memory_mk_and_salt_query(self, login):
        con = self.__get_connection()
        cur = con.cursor()

        cur.execute(
            'SELECT encrypted_control_string, salt FROM "user" WHERE login = (%s)',
            (login,)
        )
        result = cur.fetchone()

        self.__close_connection(con, cur)
        return result

    def add_new_account_query(self, login, encrypted_control_string, salt):
        con = self.__get_connection()
        cur = con.cursor()

        cur.execute(
            'INSERT INTO "user" (login, encrypted_control_string, salt) '
            'VALUES (%s, %s, %s)',
            (login, encrypted_control_string, salt)
        )
        con.commit()

        self.__close_connection(con, cur)

    def get_all_entries_query(self, user_login):
        con = self.__get_connection()
        cur = con.cursor()

        cur.execute(
            'SELECT id, service_name, login FROM account WHERE user_login = %s',
            (user_login,)
        )
        result = cur.fetchall()

        self.__close_connection(con, cur)
        return result
    
    def get_entry_password_query(self, id):
        con = self.__get_connection()
        cur = con.cursor()
        
        cur.execute(
            'SELECT encrypted_password, salt FROM account WHERE id = %s',
            (id,)
        )
        result = cur.fetchone()
        
        self.__close_connection(con, cur)
        return result
    
    def has_entry_query(self, user_login, service_name, login):
        con = self.__get_connection()
        cur = con.cursor()

        cur.execute(
            'SELECT EXISTS(SELECT 1 FROM account '
            'WHERE (user_login, service_name, login) = (%s, %s, %s))',
            (user_login, service_name, login)
        )
        result = cur.fetchone()[0]

        self.__close_connection(con, cur)
        return result

    def add_new_entry_query(
        self, user_login, service_name, login, encrypted_password, salt
    ):
        con = self.__get_connection()
        cur = con.cursor()

        cur.execute(
            'INSERT INTO account (user_login, service_name, login, '
            'encrypted_password, salt) VALUES (%s, %s, %s, %s, %s)',
            (user_login, service_name, login, encrypted_password, salt)
        )
        con.commit()

        self.__close_connection(con, cur)

    def update_entry_query(
        self, id, encrypted_password, salt
    ):
        con = self.__get_connection()
        cur = con.cursor()
        
        cur.execute(
            'UPDATE account SET (encrypted_password, salt) '
            '= (%s, %s) WHERE id = (%s)',
            (encrypted_password, salt, id)
        )
        con.commit()
        
        self.__close_connection(con, cur)

    def delete_entry_query(self, entry_id):
        con = self.__get_connection()
        cur = con.cursor()

        cur.execute('DELETE FROM account WHERE id = %s', (entry_id,))
        con.commit()

        self.__close_connection(con, cur)
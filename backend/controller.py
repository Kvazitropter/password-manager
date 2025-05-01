from backend.custom_errors import (
    ExistingLogin,
    IncorrectMasterKey,
    NonexistingLogin,
)
from backend.encrypting.decrypt import decrypt
from backend.encrypting.encrypt import encrypt


class Controller():
    def __init__(self, repository):
        self.repository = repository    

    def is_existing_login(self, login):
        return self.repository.has_login_query(login)

    def login(self, login, entered_master_key):
        self.is_existing_login(login)

        is_correct_login = self.is_existing_login(login)

        if not is_correct_login:
            raise NonexistingLogin()

        memory_mk_and_salt = self.repository.get_memory_mk_and_salt_query(login)
        salt, encrypted_master_key = (bytes(m) for m in memory_mk_and_salt)
        control_string = decrypt(entered_master_key, encrypted_master_key, salt)
        print(f'!{control_string}!')

        if control_string != 'control':
            raise IncorrectMasterKey()

    def create_new_account(self, login, master_key):
        is_existing_login = self.is_existing_login(login)

        if is_existing_login:
            raise ExistingLogin()

        encrypted_master_key, salt = encrypt(master_key)
        self.repository.add_new_account_query(login, encrypted_master_key, salt)
        
    def get_entries(self, login):
        return self.repository.get_all_entries_query(login)

    def add_new_entry(
        self, user_login, master_key, service_name, login, password
    ):
        encrypted_password, salt = encrypt(master_key, password)
        self.repository.add_new_entry_query(
            user_login, service_name, login, encrypted_password, salt
        )

    def delete_entry(self, entry_id):
        self.repository.delete_entry_query(entry_id)
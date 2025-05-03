from backend.custom_errors import (
    ExistingAccount,
    ExistingEntry,
    IncorrectMasterKey,
    NonExistingAccount,
)
from scripts.encryption import decrypt, encrypt


class Controller():
    def __init__(self, repository):
        self.repository = repository    

    def is_existing_account(self, login):
        return self.repository.has_account_query(login)

    def login(self, login, entered_master_key):
        is_existing_login = self.is_existing_account(login)

        if not is_existing_login:
            raise NonExistingAccount

        memory_mk_and_salt = self.repository.get_memory_mk_and_salt_query(login)
        encrypted_control_string, salt = (bytes(m) for m in memory_mk_and_salt)

        try:
            decrypt(entered_master_key, encrypted_control_string, salt)
        except Exception:
            raise IncorrectMasterKey

    def create_new_account(self, login, master_key):
        is_existing_account = self.is_existing_account(login)

        if is_existing_account:
            raise ExistingAccount

        encrypted_control_string, salt = encrypt(master_key)
        self.repository.add_new_account_query(login, encrypted_control_string, salt)
        
    def get_entries(self, login):
        return self.repository.get_all_entries_query(login)
    
    def get_entry_password(self, id, master_key):
        memory_passwd_and_salt = self.repository.get_entry_password_query(id)
        encrypted_password, salt = (bytes(m) for m in memory_passwd_and_salt)
        password = decrypt(master_key, encrypted_password, salt)
        return password
    
    def is_existing_entry(self, user_login, service_name, login):
        self.repository.has_entry_query(user_login, service_name, login)

    def add_new_entry(
        self, user_login, master_key, service_name, login, password
    ):
        is_existing_entry = self.is_existing_entry(
            user_login, service_name, login
        )
        
        if is_existing_entry:
            raise ExistingEntry

        encrypted_password, salt = encrypt(master_key, password)
        self.repository.add_new_entry_query(
            user_login, service_name, login, encrypted_password, salt
        )
    
    def update_entry(self, master_key, entry_id, password):  
        encrypted_password, salt = encrypt(master_key, password)
        self.repository.update_entry_query(
            entry_id, encrypted_password, salt
        )

    def delete_entry(self, entry_id):
        self.repository.delete_entry_query(entry_id)
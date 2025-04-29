# from backend import connection
from backend import mk_funcs


class Main():
    def has_master_key(self, master_key):
        return mk_funcs.has_mk(master_key)
    
    def create_new_account(self, master_key):
        is_existed_master_key = self.has_master_key(master_key)

        if is_existed_master_key:
            raise Exception('Такой мастер ключ уже существует.')
        
        try:
            mk_funcs.add_new_mk(master_key)
            return True
        except:
            raise Exception('Что-то пошло не так. Повторите попытку')
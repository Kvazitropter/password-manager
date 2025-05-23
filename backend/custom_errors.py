class ConnectionError(Exception):
    def __init__(self, message=None):
        self.message = message or 'Ошибка соединения с базой данных.'
    
    def __str__(self):
        return self.message


class IncorrectMasterKey(Exception):
    def __init__(self, message=None):
        self.message = message or 'Введённый мастер пароль неверный.'
    
    def __str__(self):
        return self.message


class NonExistingAccount(Exception):
    def __init__(self, message=None):
        self.message = message or 'Данный логин не найден.'
    
    def __str__(self):
        return self.message
    

class ExistingAccount(Exception):
    def __init__(self, message=None):
        self.message = message or 'Аккаунт с таким логином уже существует.'
    
    def __str__(self):
        return self.message


class ExistingEntry(Exception):
    def __init__(self, message=None):
        self.message = (message
            or 'Запись с таким именем сервиса и логином существует.')
    
    def __str__(self):
        return self.message
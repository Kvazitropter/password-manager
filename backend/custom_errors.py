class IncorrectMasterKey(Exception):
    def __init__(self, message):
        self.message = message or 'Введённый мастер пароль неверный.'
    
    def __str__(self):
        return self.message


class NonexistingLogin(Exception):
    def __init__(self, message):
        self.message = message or 'Данный логин не найден.'
    
    def __str__(self):
        return self.message
    

class ExistingLogin(Exception):
    def __init__(self, message):
        self.message = message or 'Аккаунт с таким логином уже существует.'
    
    def __str__(self):
        return self.message
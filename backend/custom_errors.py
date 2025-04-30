class IncorrectMasterKey(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Введённый мастер пароль неверный.'
    
    def __str__(self):
        return self.message


class NonexistingLogin(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Данный логин не найден.'
    
    def __str__(self):
        return self.message
    

class ExistingLogin(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Аккаунт с таким логином уже существует.'
    
    def __str__(self):
        return self.message
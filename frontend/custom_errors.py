class EmptyLogin(Exception):
    def __init__(self, message=None):
        self.message = (message
            or 'Логин не может быть пустым')
    
    def __str__(self):
        return self.message


class EmptyPassword(Exception):
    def __init__(self, message=None):
        self.message = (message
            or 'Пароль не может быть пустым')
    
    def __str__(self):
        return self.message


class EmptyService(Exception):
    def __init__(self, message=None):
        self.message = (message
            or 'Имя сервиса не может быть пустым')
    
    def __str__(self):
        return self.message

class SmallPasswordLength(Exception):
    def __init__(self, message, min_length):
        self.min_length = min_length
        self.message = (message
            or f"Длина пароля слишком мала. Минимум: {min_length}.")
        super().__init__(self.message)
    
    def __str__(self):
        return self.message


class NotEnoughUniqSymbols(Exception):
    def __init__(self, message, min_count):
        self.min_count = min_count
        self.message = (message
            or f"Недостаточно уникальных символов. Минимум: {min_count}.")
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
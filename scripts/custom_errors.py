class NonExistingRule(Exception):
    def __init__(self, message=None):
        self.message = message or 'Попытка установить несуществующее правило.'
    
    def __str__(self):
        return self.message


class NoSymbolsToGenerateFrom(Exception):
    def __init__(self, message=None):
        self.message = message or 'Символы для генерации отсутствуют.'
    
    def __str__(self):
        return self.message

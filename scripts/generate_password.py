import secrets

from scripts.custom_errors import NotEnoughUniqSymbols, SmallPasswordLength
from scripts.load_json import load_json

default_password_config = load_json('scripts/default_password_config.json')
symbols = load_json('scripts/symbols.json')


class PasswordGenerator():
    def __init__(self, config=default_password_config, symbols=symbols):
        self.config = config
        self.symbols = symbols
    
    def set_config(self, new_config):
        self.config = {**self.config, **new_config}
        
    def generate(self):
        (
            min_password_length, min_uniq_symbols_count, length, use_lowercase,
            use_uppercase, use_digits, use_special_symbols, custom_symbols,
        ) = self.config.values()

        if length < min_password_length:
            raise SmallPasswordLength(min_password_length)

        chars = ''.join(set(custom_symbols))

        if use_lowercase:
            chars += self.symbols['lowercase_letters']
    
        if use_uppercase:
            chars += self.symbols['uppercase_letters']
        
        if use_digits:
            chars += self.symbols['digits']
            
        if use_special_symbols:
            chars += self.symbols['special_symbols']
            
        if len(chars) < min_uniq_symbols_count:
            raise NotEnoughUniqSymbols(min_uniq_symbols_count)

        return ''.join(secrets.choice(chars) for _ in range(length))

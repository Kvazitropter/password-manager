import secrets

from load_json import load_json

default_password_config = load_json('scripts/default_password_config.json')
symbols = load_json('scripts/symbols.json')


class PasswordGenerator():
    def __init__(self, config=default_password_config, symbols=symbols):
        self.config = config
        self.symbols = symbols
    
    def set_config(self, new_config):
        self.config = {**self.config, **new_config}
        
    def generate(self):
        length, *rest_settings, custom_symbols = self.config.values()
        uniq_custom_symbols = ''.join(set(custom_symbols))
        (
            use_lowercase, use_uppercase, use_digits, use_special_symbols
        ) = rest_settings
        
        # if length < min_password_length:
        #     raise Exception('Слишком короткий пароль.')
    
        # if (not any(rest_settings)
        #         and len(uniq_custom_symbols) < min_uniq_symbols_count):
        #     raise Exception('Недостаточно символов для генерации')
        
        chars = uniq_custom_symbols
        
        if use_lowercase:
            chars += self.symbols['lowercase_letters']
    
        if use_uppercase:
            chars += self.symbols['uppercase_letters']
        
        if use_digits:
            chars += self.symbols['digits']
            
        if use_special_symbols:
            chars += self.symbols['special_symbols']
        print(chars)
        
        return ''.join(secrets.choice(chars) for _ in range(length))

import secrets

from scripts.load_json import load_json
import re


class PasswordGenerator():
    def __init__(self, config=None, symbols=None):
        self.config = config or load_json('scripts/default_password_config.json')
        self.default_config = self.config
        self.symbols = symbols or load_json('scripts/symbols.json')
        self.setup_for_generating()

    def set_rule(self, rule, value):
        self.config[rule] = value
        self.setup_for_generating()

    def reset_default_config(self):
        self.config = self.default_config
        self.setup_for_generating()

    def setup_for_generating(self):
        (
            _, use_lowercase, use_uppercase, use_digits,
            use_special_symbols, custom_symbols,
        ) = self.config.values()
        chars = ''.join(set(custom_symbols))
        regexp_groups = [f'[{chars}]+'] if chars else []

        if use_lowercase:
            chars += self.symbols['lowercase_letters']
            regexp_groups.append('[a-z]+')
    
        if use_uppercase:
            chars += self.symbols['uppercase_letters']
            regexp_groups.append('[A-Z]+')
        
        if use_digits:
            chars += self.symbols['digits']
            regexp_groups.append('[0-9]+')
            
        if use_special_symbols:
            chars += self.symbols['special_symbols']
            regexp_groups.append('[!@#$%^&*?]+')

        self.chars = chars
        self.regexp_groups = regexp_groups
    
    def check_password(self, password):
        print(self.regexp_groups, password)
        return all(re.compile(regexp).search(password) for regexp in self.regexp_groups)

    def generate(self):
        length = self.config['length']
        while True:
            password = ''.join(secrets.choice(self.chars) for _ in range(length))
            if self.check_password(password):
                return password

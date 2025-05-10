import json
import re
import secrets

from scripts.custom_errors import NonExistingRule, NoSymbolsToGenerateFrom
from scripts.path_helper import get_base_config_path


class PasswordGenerator():
    def __init__(self):
        json_config_path = get_base_config_path(
            'scripts/default_password_config.json')
        with open(json_config_path, 'r') as file:
            self.default_config = json.loads(file.read())
        self.config = self.default_config.copy()
        self.__setup_for_generating()

    def set_config(self, config):
        rules = config.keys()
        for rule in rules:
            if rule not in self.default_config:
                raise NonExistingRule       

        self.config = {**self.config, **config}
        self.__setup_for_generating()
        
    def get_config(self):
        return self.config

    def get_default_config(self):
        return self.default_config

    def reset_default_config(self):
        self.config = self.default_config
        self.__setup_for_generating()

    def __setup_for_generating(self):
        (
            _, use_lowercase, use_uppercase, use_digits,
            use_special_symbols, custom_symbols,
        ) = self.config.values()
        uniq_custom_symbols = ''.join(set(custom_symbols))

        self.chars = ''
        self.regexp_groups = []

        if use_lowercase:
            self.chars += 'abcdefghijklnopqrstuvwxyz'
            self.regexp_groups.append('[a-z]+')
    
        if use_uppercase:
            self.chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            self.regexp_groups.append('[A-Z]+')
        
        if use_digits:
            self.chars += '1234567890'
            self.regexp_groups.append('[0-9]+')
            
        if use_special_symbols:
            self.chars += '!@#$%^&*?'
            self.regexp_groups.append('[!@#$%^&*?]+')

        if uniq_custom_symbols:
            self.chars += uniq_custom_symbols
            self.regexp_groups.append(f'[{uniq_custom_symbols}]+')
        
        if not self.chars:
            raise NoSymbolsToGenerateFrom
    
    def __check_password(self, password):
        return all(
            re.compile(regexp).search(password) for regexp in self.regexp_groups
        )

    def generate(self):
        length = self.config['length']

        if length == 0:
            return ''

        while True:
            password = ''.join(
                secrets.choice(self.chars) for _ in range(length)
            )
            if self.__check_password(password):
                return password

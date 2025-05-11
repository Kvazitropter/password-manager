import pytest

from scripts.custom_errors import NonExistingRule, NoSymbolsToGenerateFrom
from scripts.generate_password import PasswordGenerator


def has_intersection(str1, str2):
    return not set(str1).isdisjoint(str2)


@pytest.fixture
def default_config():
    return {
        'length': 12,
        'use_lowercase': True,
        'use_uppercase': True,
        'use_digits': True,
        'use_special_symbols': True,
        'custom_symbols': ''
    }


@pytest.fixture
def special_symbols():
    return '!@#$%^&*?'


@pytest.fixture
def generator():
    return PasswordGenerator()


def test_generator_with_default_params(generator,
        default_config, special_symbols):
    assert generator.get_default_config() == default_config
    assert generator.get_config() == default_config
    
    password = generator.generate()

    assert len(password) == default_config['length']
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert has_intersection(password, special_symbols)


def test_generator_set_length(generator):
    generator.set_config({'length': 20})
    config = generator.get_config()
    password = generator.generate()

    assert config['length'] == 20
    assert len(password) == 20
    

def test_generator_disable_use_lowercase(generator):
    generator.set_config({'use_lowercase': False})
    config = generator.get_config()
    password = generator.generate()

    assert not config['use_lowercase']
    assert not any(c.islower() for c in password)


def test_generator_disable_use_uppercase(generator):
    generator.set_config({'use_uppercase': False})
    config = generator.get_config()
    password = generator.generate()

    assert not config['use_uppercase']
    assert not any(c.isupper() for c in password)


def test_generator_disable_use_digits(generator):
    generator.set_config({'use_digits': False})
    config = generator.get_config()
    password = generator.generate()

    assert not config['use_digits']
    assert not any(c.isdigit() for c in password)


def test_generator_disable_use_special(generator, special_symbols):
    generator.set_config({'use_special_symbols': False})
    config = generator.get_config()
    password = generator.generate()

    assert not config['use_special_symbols']
    assert not has_intersection(password, special_symbols)


def test_generator_set_custom_symbols(generator):
    custom_symbols = ':_)'
    generator.set_config({'custom_symbols': custom_symbols})
    config = generator.get_config()
    password = generator.generate()

    assert config['custom_symbols'] == custom_symbols
    assert has_intersection(password, custom_symbols)


def test_generator_set_nonexist_rule(generator):    
    with pytest.raises(NonExistingRule):
        generator.set_config({'some_rule': True})


def test_generator_reset_config(generator, default_config):
    changed_config = {
        'length': 99,
        'use_lowercase': False,
        'use_uppercase': False,
        'use_digits': False,
        'use_special_symbols': False,
        'custom_symbols': ':_)',
    }
    generator.set_config(changed_config)

    assert generator.get_config() == changed_config
    generator.reset_default_config()
    assert generator.get_config() == default_config


def test_generator_all_rules_disabled(generator):
    all_rules_disabled_config = {
        'use_lowercase': False,
        'use_uppercase': False,
        'use_digits': False,
        'use_special_symbols': False,
    }

    with pytest.raises(NoSymbolsToGenerateFrom):
        generator.set_config(all_rules_disabled_config)


def test_generator_set_empty_config(generator, default_config):
    generator.set_config({})

    assert generator.get_config() == default_config


def test_generator_zero_length(generator):
    generator.set_config({'length': 0})
    password = generator.generate()

    assert password == ''


def test_generator_large_length(generator):
    large_length = 100000
    generator.set_config({'length': large_length})
    password = generator.generate()

    assert len(password) == large_length
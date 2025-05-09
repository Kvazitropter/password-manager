from unittest.mock import MagicMock

import pytest
from PyQt6.QtWidgets import QApplication

from backend.custom_errors import (
    ExistingEntry,
    NonExistingAccount,
)
from frontend.custom_errors import (
    EmptyLogin,
    EmptyPassword,
    EmptyService,
)
from frontend.main import PasswordManager


@pytest.fixture
def passwd_manager():
    controller = MagicMock()
    generator = MagicMock()
    generator.get_config.return_value = {
        "length": 12,
        "use_lowercase": True,
        "use_uppercase": True,
        "use_digits": True,
        "use_special_symbols": True,
        "custom_symbols": ""
    }
    view = MagicMock()
    window = PasswordManager(controller, generator, view)
    return window, controller, view

         
def test_login(passwd_manager):
    window, controller, view = passwd_manager
    window.open_login_window()
    view.ui_login.input_login.text.return_value = 'login'
    view.ui_login.input_master_key.text.return_value = 'mymasterkey'
    window.login()
    controller.login.assert_called_once_with('login', 'mymasterkey')
    view.start_window.close.assert_called_once()
    view.login_window.close.assert_called_once()


def test_wrong_login(passwd_manager):
    window, controller, view = passwd_manager
    view.ui_login.input_login.text.return_value = 'wrong_login'
    view.ui_login.input_master_key.text.return_value = 'master_key'
    controller.login.side_effect = NonExistingAccount('Данный логин не найден.')
    window.open_login_window()
    window.login()
    view.show_invalid_input.assert_called_once()


@pytest.mark.parametrize('login, mk, error, label, expected_input', [
    ('', 'passwd', EmptyLogin, 'label_feedback_login', 'input_login'),
    ('login', '', EmptyPassword, 'label_feedback_master_key', 'input_master_key'),
])
def test_login_empty(passwd_manager, login, mk, error, label, expected_input):
    window, _, view = passwd_manager
    view.ui_login.input_login.text.return_value = login
    view.ui_login.input_master_key.text.return_value = mk
    window.login()
    input = getattr(view.ui_login, expected_input)
    fb_label = getattr(view.ui_login, label)
    view.show_invalid_input.assert_called_once_with(input, fb_label, str(error()))


def test_signup(passwd_manager):
    window, controller, view = passwd_manager
    window.open_signup_window()
    view.ui_signup.input_new_login.text.return_value = 'boba'
    view.ui_signup.input_new_master_key.text.return_value = 'qqq111'
    window.signup()
    controller.create_new_account.assert_called_once_with('boba', 'qqq111')


def test_logout(passwd_manager):
    window, _, view = passwd_manager
    window.master_key = 'www222!'
    window.user_login = 'biba'
    window.logout()
    assert window.master_key is None
    assert window.user_login is None
    view.close.assert_called_once()
    view.setup_start_window.assert_called_once()


def test_add_entry(passwd_manager):
    window, controller, view = passwd_manager
    window.open_new_entry_window()
    window.user_login = 'ivan'
    window.master_key = 'key'
    view.ui_new_entry.input_service_name.text.return_value = 'Helix'
    view.ui_new_entry.input_login.text.return_value = 'ivan124'
    view.ui_new_entry.input_password.text.return_value = 'passwd'
    window.view_entries = MagicMock()
    window.new_entry()
    controller.add_new_entry.assert_called_once_with(
        'ivan', 'key', 'Helix', 'ivan124', 'passwd'
    )
    view.view_entries.assert_called_once()


@pytest.mark.parametrize('site, login, passwd, error, label, input', [
    ('', 'bob', 'pas', EmptyService, 'label_feedback_s_name', 'input_service_name'),
    ('skype', '', 'pas', EmptyLogin, 'label_feedback_login', 'input_login'),
    ('skype', 'bob', '', EmptyPassword, 'label_feedback_password', 'input_password'),
])
def test_new_entry_empty(passwd_manager, site, login, passwd,
                        error, label, input):
    window, _, view = passwd_manager
    view.ui_new_entry.input_service_name.text.return_value = site
    view.ui_new_entry.input_login.text.return_value = login
    view.ui_new_entry.input_password.text.return_value = passwd
    window.new_entry()
    input = getattr(view.ui_new_entry, input)
    fb_label = getattr(view.ui_new_entry, label)
    view.show_invalid_input.assert_called_once_with(input, fb_label,
                                                    str(error()))


def test_entry_exists(passwd_manager):
    window, controller, view = passwd_manager
    exception = ExistingEntry(
        'Запись с таким именем сервиса и логином уже существует.'
    )
    controller.add_new_entry.side_effect = exception
    view.ui_new_entry.input_service_name.text.return_value = 'existing_service'
    view.ui_new_entry.input_login.text.return_value = 'existing_login'
    view.ui_new_entry.input_password.text.return_value = 'passwd'
    window.user_login = 'ivan'
    window.master_key = 'key'
    window.new_entry()
    view.show_invalid_input.assert_any_call(
        view.ui_new_entry.input_service_name,
        view.ui_new_entry.label_feedback_s_name,
        str(exception)
    )


def test_generate_and_insert_password(passwd_manager):
    window, _, view = passwd_manager
    input = MagicMock()
    view.ui_new_entry.input_password = input
    window.generator.generate.return_value = 'generated!pass'
    window.generate_and_insert_password(input)
    window.view.set_input_text.assert_called_once_with(input, 'generated!pass')


def test_toggle_password_visibility(passwd_manager):
    window, _, view = passwd_manager
    input = MagicMock()
    window.toggle_password_visibility(True, input)
    view.show_password.assert_called_once_with(input)
    window.toggle_password_visibility(False, input)
    view.hide_password.assert_called_once_with(input)


def test_copy_password(passwd_manager, qtbot):
    window, _, _ = passwd_manager
    window.open_new_entry_window()
    input = MagicMock()
    input.text.return_value = 'passwd'
    clipboard = QApplication.clipboard()
    clipboard.clear()
    window.copy_password(input)
    assert clipboard.text() == 'passwd'


def test_edit_entry(passwd_manager):
    window, controller, view = passwd_manager
    window.master_key = 'key'
    input = MagicMock()
    input.text.return_value = 'new_password'
    view.ui_entry.input_password = input
    view.ui_entry.label_feedback_password = MagicMock()
    window.view.edit_entry_window = MagicMock()
    window.update_entries = MagicMock()
    window.edit_entry(1)
    controller.update_entry.assert_called_once_with('key', 1, 'new_password')
    window.view.edit_entry_window.close.assert_called_once()
    window.update_entries.assert_called_once()


def test_delete_entry(passwd_manager):
    window, controller, _ = passwd_manager
    controller.delete_entry = MagicMock()
    controller.update_entry = MagicMock()
    window.update_entries = MagicMock() 
    window.user_login = 'ivan' 
    window.delete_entry(1)
    controller.delete_entry.assert_called_once_with(1)
    window.update_entries.assert_called_once()


def test_password_settings(passwd_manager):
    window, _, view = passwd_manager
    view.ui_settings.spinbox_length.value.return_value = 12
    view.ui_settings.checkbox_lcase.isChecked.return_value = True
    view.ui_settings.checkbox_upcase.isChecked.return_value = True
    view.ui_settings.checkbox_digits.isChecked.return_value = True
    view.ui_settings.checkbox_symbols.isChecked.return_value = True
    view.ui_settings.input_custom.text.return_value = ''
    window.password_settings()
    window.generator.set_config.assert_called_once_with({
        "length": 12,
        "use_lowercase": True,
        "use_uppercase": True,
        "use_digits": True,
        "use_special_symbols": True,
        "custom_symbols": ""
    })
    view.password_settings_window.close.assert_called_once()

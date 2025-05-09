from unittest.mock import MagicMock

import pytest
from PyQt6.QtWidgets import QLineEdit

from frontend.view import PasswordManagerView


@pytest.fixture
def passwd_manager_view(qtbot):
    view = PasswordManagerView()
    qtbot.addWidget(view)
    return view


def test_setup_all_windows(passwd_manager_view):
    passwd_manager_view.setup_start_window()
    assert passwd_manager_view.start_window.isModal()
    passwd_manager_view.setup_login_window()
    assert passwd_manager_view.login_window.isModal()
    passwd_manager_view.setup_signup_window()
    assert passwd_manager_view.signup_window.isModal()
    passwd_manager_view.setup_new_entry_window()
    assert passwd_manager_view.new_entry_window.isModal()        


def test_setup_entry_window(passwd_manager_view):
    passwd_manager_view.setup_entry_window('frepng', 'loglog', 'passwd')
    assert passwd_manager_view.ui_entry.input_service_name.text() == 'frepng'
    assert passwd_manager_view.ui_entry.input_service_name.isReadOnly()
    assert passwd_manager_view.ui_entry.input_login.text() == 'loglog'
    assert passwd_manager_view.ui_entry.input_login.isReadOnly()
    assert passwd_manager_view.ui_entry.input_password.text() == 'passwd'


def test_show_and_remove_invalid_input(passwd_manager_view):
    passwd_manager_view.setup_signup_window()
    my_input = passwd_manager_view.ui_signup.input_new_login
    fb_label = passwd_manager_view.ui_signup.label_feedback_login
    passwd_manager_view.show_invalid_input(my_input, fb_label, "Ошибка")
    assert "f54021" in my_input.styleSheet()
    assert fb_label.text() == "Ошибка"
    passwd_manager_view.remove_invalid_input(my_input, fb_label)
    assert "f54021" not in my_input.styleSheet()
    assert fb_label.text() == ""


def test_view_entries_with_btns(passwd_manager_view):
    passwd_manager_view.setup_main_window()
    show_cb = MagicMock()
    delete_cb = MagicMock()
    storage = passwd_manager_view.ui_main.table_entries
    passwd_manager_view.view_entries([
        (1, 'youtube', 'ivanivan'),
    ], show_cb, delete_cb)    
    assert storage.rowCount() == 1
    assert storage.item(0, 0).text() == 'youtube'
    assert storage.item(0, 1).text() == 'ivanivan'
    edit_entry = storage.cellWidget(0, 2)
    delete_entry_button = storage.cellWidget(0, 3)
    edit_entry.click()
    show_cb.assert_called_once_with('youtube', 'ivanivan', 1)
    delete_entry_button.click()
    delete_cb.assert_called_once_with(1)

   
def test_setup_password_settings_values(passwd_manager_view):
    config = {
        "length": 8,
        "use_lowercase": True,
        "use_uppercase": False,
        "use_digits": True,
        "use_special_symbols": True,
        "custom_symbols": "@$&"
    }
    passwd_manager_view.setup_password_settings_window(config)
    assert passwd_manager_view.ui_settings.spinbox_length.value() == 8
    assert passwd_manager_view.ui_settings.checkbox_lcase.isChecked()
    assert not passwd_manager_view.ui_settings.checkbox_upcase.isChecked()
    assert passwd_manager_view.ui_settings.checkbox_digits.isChecked()
    assert passwd_manager_view.ui_settings.checkbox_symbols.isChecked()
    assert passwd_manager_view.ui_settings.input_custom.text() == '@$&'


def test_switch_password_echo_mode(passwd_manager_view):
    passwd_manager_view.setup_new_entry_window()
    my_input = passwd_manager_view.ui_new_entry.input_password
    passwd_manager_view.hide_password(my_input)
    assert my_input.echoMode() == QLineEdit.EchoMode.Password
    passwd_manager_view.show_password(my_input)
    assert my_input.echoMode() == QLineEdit.EchoMode.Normal

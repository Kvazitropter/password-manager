from PyQt6.QtWidgets import QApplication

from backend.custom_errors import (
    ExistingAccount,
    ExistingEntry,
    IncorrectMasterKey,
    NonExistingAccount,
)
from frontend.custom_errors import EmptyLogin, EmptyPassword, EmptyService


class PasswordManager:
    def __init__(self, controller, generator, view):
        self.controller = controller
        self.generator = generator
        self.view = view

    def show(self):
        self.open_start_window()

    def open_start_window(self):
        self.view.setup_start_window()
        self.view.ui_start.btn_login.clicked.connect(self.open_login_window)
        self.view.ui_start.btn_signup.clicked.connect(self.open_signup_window)
        self.view.start_window.show()

    def open_login_window(self):
        self.view.setup_login_window()
        self.view.login_window.show()
        self.view.ui_login.btn_submit_login.clicked.connect(self.login)

    def open_signup_window(self):
        self.view.setup_signup_window()
        self.view.signup_window.show()
        self.view.ui_signup.btn_submit_signup.clicked.connect(self.signup)

    def open_main_window(self):
        self.view.setup_main_window()
        self.update_entries()
        self.view.show()

        self.view.ui_main.btn_exit.clicked.connect(self.logout)
        self.view.ui_main.btn_new_entry.clicked.connect(
            self.open_new_entry_window)
            
    def open_new_entry_window(self):
        self.view.setup_new_entry_window()
        self.view.new_entry_window.show()

        self.view.ui_new_entry.btn_generate_password.clicked.connect(
            lambda: self.generate_and_insert_password(
                self.view.ui_new_entry.input_password
            ))
        self.view.ui_new_entry.btn_submit_entry.clicked.connect(
            self.new_entry)
        self.view.ui_new_entry.btn_show.clicked.connect(
            lambda is_checked, *_: self.toggle_password_visibility(
                is_checked, self.view.ui_new_entry.input_password
            ))
        self.view.ui_new_entry.btn_copy.clicked.connect(
            lambda: self.copy_password(
                self.view.ui_new_entry.input_password))
        self.view.ui_new_entry.btn_settings.clicked.connect(
            self.open_password_settings_window)

    def open_edit_entry_window(self, service_name, login, id):
        password = self.controller.get_entry_password(id, self.master_key)
        self.view.setup_entry_window(service_name, login, password)
        self.view.edit_entry_window.show()

        self.view.ui_entry.btn_generate_password.clicked.connect(
            lambda: self.generate_and_insert_password(
                self.view.ui_entry.input_password))
        self.view.ui_entry.btn_submit_entry.clicked.connect(lambda: 
            self.edit_entry(id))
        self.view.ui_entry.btn_show.clicked.connect(
            lambda is_checked, *_: self.toggle_password_visibility(
                is_checked, self.view.ui_new_entry.input_password))
        self.view.ui_entry.btn_copy.clicked.connect(
            lambda: self.copy_password(
                self.view.ui_new_entry.input_password))
        self.view.ui_entry.btn_settings.clicked.connect(
            self.open_password_settings_window)

    def open_password_settings_window(self):
        config = self.generator.get_config()
        self.view.setup_password_settings_window(config)
        self.view.ui_settings.btn_submit_settings.clicked.connect(
            self.password_settings)
        self.view.ui_settings.btn_reset.clicked.connect(
            self.reset_generating_config)
        self.view.password_settings_window.show()

    def login(self):
        user_login = self.view.ui_login.input_login.text()
        master_key = self.view.ui_login.input_master_key.text()
        
        try:
            self.view.remove_invalid_input(
                self.view.ui_login.input_login,
                self.view.ui_login.label_feedback_login)
            self.view.remove_invalid_input(
                self.view.ui_login.input_master_key,
                self.view.ui_login.label_feedback_master_key)
            if not user_login:
                raise EmptyLogin
            if not master_key:
                raise EmptyPassword
            self.controller.login(user_login, master_key)
            self.master_key = master_key
            self.user_login = user_login
            self.open_main_window()
            self.view.start_window.close()
            self.view.login_window.close()
        except (NonExistingAccount, EmptyLogin) as e:
            self.view.show_invalid_input(
                self.view.ui_login.input_login,
                self.view.ui_login.label_feedback_login, str(e))
        except (IncorrectMasterKey, EmptyPassword) as e:
            self.view.show_invalid_input(
                self.view.ui_login.input_master_key,
                self.view.ui_login.label_feedback_master_key, str(e))

    def signup(self):
        new_login = self.view.ui_signup.input_new_login.text()
        new_master_key = self.view.ui_signup.input_new_master_key.text()

        try:
            self.view.remove_invalid_input(
                self.view.ui_signup.input_new_login,
                self.view.ui_signup.label_feedback_login)
            self.view.remove_invalid_input(
                self.view.ui_signup.input_new_master_key,
                self.view.ui_signup.label_feedback_master_key)
            if not new_login:
                raise EmptyLogin
            if not new_master_key:
                raise EmptyPassword
            self.controller.create_new_account(new_login, new_master_key)
            self.master_key = new_master_key
            self.user_login = new_login
            self.open_main_window()
            self.view.start_window.close()
            self.view.signup_window.close()
        except (ExistingAccount, EmptyLogin) as e:
            self.view.show_invalid_input(
                self.view.ui_signup.input_new_login,
                self.view.ui_signup.label_feedback_login, str(e))
        except (EmptyPassword, Exception) as e:
            self.view.show_invalid_input(
                self.view.ui_signup.input_new_master_key,
                self.view.ui_signup.label_feedback_master_key, str(e))

    def update_entries(self):
        entries = self.controller.get_entries(self.user_login)
        self.view.view_entries(entries, self.open_edit_entry_window,
                            self.delete_entry)

    def new_entry(self):
        service_name = self.view.ui_new_entry.input_service_name.text()
        login = self.view.ui_new_entry.input_login.text()
        password = self.view.ui_new_entry.input_password.text()
        
        try:
            self.view.remove_invalid_input(
                self.view.ui_new_entry.input_service_name,
                self.view.ui_new_entry.label_feedback_s_name)
            self.view.remove_invalid_input(
                self.view.ui_new_entry.input_login,
                self.view.ui_new_entry.label_feedback_login)
            self.view.remove_invalid_input(
                self.view.ui_new_entry.input_password,
                self.view.ui_new_entry.label_feedback_password)
            if not service_name:
                raise EmptyService
            if not login:
                raise EmptyLogin
            if not password:
                raise EmptyPassword
            self.controller.add_new_entry(
                self.user_login, self.master_key, service_name, login, password
            )
            self.view.new_entry_window.close()
            self.update_entries()
        except (ExistingEntry, EmptyService, EmptyLogin) as e:
            if isinstance(e, (ExistingEntry, EmptyService)):
                self.view.show_invalid_input(
                    self.view.ui_new_entry.input_service_name,
                    self.view.ui_new_entry.label_feedback_s_name, str(e))
            if isinstance(e, (ExistingEntry, EmptyLogin)):
                self.view.show_invalid_input(
                    self.view.ui_new_entry.input_login,
                    self.view.ui_new_entry.label_feedback_login, str(e))
        except (EmptyPassword, Exception) as e:
            self.view.show_invalid_input(
                self.view.ui_new_entry.input_password,
                self.view.ui_new_entry.label_feedback_password, str(e))

    def edit_entry(self, id):
        new_password = self.view.ui_entry.input_password.text()

        try:
            if not new_password:
                raise EmptyPassword
            self.controller.update_entry(self.master_key, id, new_password)
            self.view.edit_entry_window.close()
            self.update_entries()
        except Exception as e:
            self.view.show_invalid_input(
                self.view.ui_entry.input_password,
                self.view.ui_entry.label_feedback_password, str(e))
    
    def delete_entry(self, id):
        self.controller.delete_entry(id)
        self.update_entries()

    def logout(self):
        self.master_key = None
        self.user_login = None
        self.open_start_window()
        self.view.close()

    def password_settings(self):
        length = self.view.ui_settings.spinbox_length.value()
        use_lowercase = self.view.ui_settings.checkbox_lcase.isChecked()
        use_uppercase = self.view.ui_settings.checkbox_upcase.isChecked()
        use_digits = self.view.ui_settings.checkbox_digits.isChecked()
        use_special = self.view.ui_settings.checkbox_symbols.isChecked()
        custom = self.view.ui_settings.input_custom.text()
        new_config = {
            'length': length,
            'use_lowercase': use_lowercase,
            'use_uppercase': use_uppercase,
            'use_digits': use_digits,
            'use_special_symbols': use_special,
            'custom_symbols': custom
        }
        
        try:
            self.generator.set_config(new_config)
            self.view.password_settings_window.close()
        except Exception as e:
            self.view.set_feedback_message(
                self.view.ui_settings.label_feedback, str(e))

    def toggle_password_visibility(self, is_checked, input):
        if is_checked:
            self.view.show_password(input)
        else:
            self.view.hide_password(input)
            
    def copy_password(self, input):
        clipboard = QApplication.clipboard()
        clipboard.setText(input.text())

    def generate_and_insert_password(self, input):
        generated_password = self.generator.generate()
        self.view.set_input_text(input, generated_password)
    
    def reset_generating_config(self):
        self.generator.reset_default_config()
        default_config = self.generator.get_config()
        self.view.setup_password_settings_window(default_config)
        self.open_password_settings_window()
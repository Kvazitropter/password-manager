from PyQt6 import QtWidgets
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow

from backend.custom_errors import (
    ExistingAccount,
    ExistingEntry,
    NonExistingAccount,
)
from frontend.pm_login import Ui_dialog_login
from frontend.pm_main_window import Ui_main_window
from frontend.pm_new_entry import Ui_dialog_new_entry
from frontend.pm_password_settings import Ui_password_settings
from frontend.pm_signup import Ui_dialog_signup
from frontend.pm_start import Ui_dialog_start


class PasswordManager(QMainWindow):
    def __init__(self, controller, generator):
        super(PasswordManager, self).__init__()
        self.controller = controller
        self.generator = generator
        self.open_start_window()
        
    def setup_main_window(self, ui):
        self.ui = ui()
        self.ui.setupUi(self)
        
        point = QPoint()
        point.setX(QApplication.primaryScreen().geometry().center()
                   .x() - self.width() // 2)
        point.setY(QApplication.primaryScreen().geometry().center()
                   .y() - self.height() // 2)
        self.move(point)
    
    def setup_dialog_window(self, ui):
        window = QtWidgets.QDialog()
        self.ui_window = ui()
        self.ui_window.setupUi(window)
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        return window
    
    def setup_extra_window(self, ui):
        window = QtWidgets.QDialog()
        ui_window = ui()
        ui_window.setupUi(window)
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        return window, ui_window

    def open_start_window(self):
        self.setCentralWidget(None)
        self.setup_main_window(Ui_dialog_start)
        self.ui.btn_login.clicked.connect(self.open_login_window)
        self.ui.btn_signup.clicked.connect(self.open_signup_window)

    def open_login_window(self):
        self.login_window = self.setup_dialog_window(Ui_dialog_login)
        self.login_window.show()
        self.ui_window.btn_submit_master_key.clicked.connect(
            lambda:
            self.check_inputs(self.login, 
                              self.ui_window.input_login,
                              self.ui_window.input_master_key))

    def open_signup_window(self):
        self.signup_window = self.setup_dialog_window(
            Ui_dialog_signup
        )
        self.signup_window.show()

        self.ui_window.btn_submit_new_master_key.clicked.connect(
            lambda: self.check_inputs(self.signup,
                              self.ui_window.input_new_master_key, 
                              self.ui_window.input_new_login))

    def open_main_window(self):
        # self.adjustSize()
        self.setup_main_window(Ui_main_window)
        self.view_entries()

        self.ui.btn_exit.clicked.connect(self.logout)
        self.ui.btn_new_entry.clicked.connect(self.open_new_entry_window)
            
    def open_new_entry_window(self):
        self.new_entry_window = self.setup_dialog_window(
            Ui_dialog_new_entry
        )
        self.new_entry_window.show()

        self.ui_window.btn_generate_password.clicked.connect(
            self.generate_and_insert_password
        )

        self.ui_window.btn_submit_entry.clicked.connect(
            lambda: self.check_inputs(self.new_entry,
                              self.ui_window.input_service_name,
                              self.ui_window.input_login,
                              self.ui_window.input_password))

        self.ui_window.btn_show.clicked.connect(
            self.toggle_password_visibility
        )
        self.ui_window.btn_copy.clicked.connect(self.copy_password)
        self.ui_window.btn_settings.clicked.connect(
            self.open_password_settings_window
        )

    def open_edit_entry_window(self, service_name, login, id):
        self.edit_entry_window = self.setup_dialog_window(
            Ui_dialog_new_entry
        )
        password = self.controller.get_entry_password(id, self.master_key)
        self.ui_window.input_service_name.setText(service_name)
        self.ui_window.input_service_name.setReadOnly(True)
        self.ui_window.input_login.setText(login)
        self.ui_window.input_login.setReadOnly(True)
        self.ui_window.input_password.setText(password)
        self.edit_entry_window.show()

        self.ui_window.btn_generate_password.clicked.connect(
            self.generate_and_insert_password)
        self.ui_window.btn_submit_entry.clicked.connect(lambda: 
            self.edit_entry(id))

        self.ui_window.btn_show.clicked.connect(self.toggle_password_visibility)
        self.ui_window.btn_copy.clicked.connect(self.copy_password)
        self.ui_window.btn_settings.clicked.connect(
            self.open_password_settings_window
        )

    def open_password_settings_window(self):
        window, ui_window = self.setup_extra_window(
            Ui_password_settings
        )
        self.password_settings_window = window
        self.ui_window_settings = ui_window
        config = self.generator.get_config()
        self.ui_window_settings.spinbox_length.setValue(config['length'])
        self.ui_window_settings.checkbox_lcase.setChecked(config['use_lowercase'])
        self.ui_window_settings.checkbox_upcase.setChecked(config['use_uppercase'])
        self.ui_window_settings.checkbox_digits.setChecked(config['use_digits'])
        self.ui_window_settings.checkbox_symbols.setChecked(config['use_special_symbols'])
        self.ui_window_settings.input_custom.setText(config['custom_symbols'])
        self.ui_window_settings.btn_submit_settings.clicked.connect(
            self.password_settings
        )
        self.password_settings_window.show()

    def login(self):
        user_login = self.ui_window.input_login.text()
        master_key = self.ui_window.input_master_key.text()
        
        try:
            self.ui_window.label_feedback_master_key.setText('')
            self.ui_window.label_feedback_login.setText('')
            self.controller.login(user_login, master_key)
            self.master_key = master_key
            self.user_login = user_login
            self.login_window.close()
            self.open_main_window()
        except NonExistingAccount as e:
            self.set_feedback_message(
                self.ui_window.label_feedback_login, str(e)
            )
        except Exception as e:
            self.set_feedback_message(
                self.ui_window.label_feedback_master_key, str(e)
            )

    def signup(self):
        new_login = self.ui_window.input_new_login.text()
        new_master_key = self.ui_window.input_new_master_key.text()

        try:
            self.controller.create_new_account(new_login, new_master_key)
            self.master_key = new_master_key
            self.user_login = new_login
            self.signup_window.close()
            self.open_main_window()
        except ExistingAccount as e:
            self.set_feedback_message(
                self.ui_window.label_feedback_login, str(e)
            )
        except Exception as e:
            self.set_feedback_message(
                self.ui_window.label_feedback_master_key, str(e)
            )

    def view_entries(self):
        self.ui.table_entries.setRowCount(0)
        entries = self.controller.get_entries(self.user_login)
        for row_num, (id, service_name, login) in enumerate(entries):
            self.ui.table_entries.insertRow(row_num)
            self.ui.table_entries.setItem(
                row_num, 0, QtWidgets.QTableWidgetItem(service_name))
            self.ui.table_entries.setItem(
                row_num, 1, QtWidgets.QTableWidgetItem(login))

            edit_entry = QtWidgets.QPushButton('Просмотр')
            edit_entry.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            edit_entry.clicked.connect(
                lambda: self.open_edit_entry_window(service_name, login, id)
            )
            self.ui.table_entries.setCellWidget(row_num, 2, edit_entry)

            delete_entry_button = QtWidgets.QPushButton('Удалить')
            delete_entry_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            delete_entry_button.clicked.connect(lambda: self.delete_entry(id))
            self.ui.table_entries.setCellWidget(row_num, 3, delete_entry_button)

    def new_entry(self):
        service_name = self.ui_window.input_service_name.text()
        login = self.ui_window.input_login.text()
        password = self.ui_window.input_password.text()
        
        try:
            self.controller.add_new_entry(
                self.user_login, self.master_key, service_name, login, password
            )
            self.view_entries()
            self.new_entry_window.close()
        except ExistingEntry as e:
            self.set_feedback_message(
                self.ui_window.label_feedback_s_name, str(e)
            )
            self.set_feedback_message(
                self.ui_window.label_feedback_login, str(e)
            )
        except Exception as e:
            self.set_feedback_message(
                self.ui_window.label_feedback_password, str(e)
            )

    def edit_entry(self, id):
        new_password = self.ui_window.input_password.text()

        try:
            self.controller.update_entry(self.master_key, id, new_password)
            self.view_entries()
            self.edit_entry_window.close()
        except Exception as e:
            self.ui_window.label_feedback.setText(str(e))
            self.ui_window.label_feedback.setToolTip(str(e))
    
    def delete_entry(self, id):
        self.controller.delete_entry(id)
        self.view_entries()

    def logout(self):
        self.master_key = None
        self.user_login = None
        self.open_start_window()

    def password_settings(self):
        length = self.ui_window_settings.spinbox_length.value()
        use_lowercase = self.ui_window_settings.checkbox_lcase.isChecked()
        use_uppercase = self.ui_window_settings.checkbox_upcase.isChecked()
        use_digits = self.ui_window_settings.checkbox_digits.isChecked()
        use_special = self.ui_window_settings.checkbox_symbols.isChecked()
        custom = self.ui_window_settings.input_custom.text()
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
            self.password_settings_window.close()
        except Exception as e:
            self.ui_window_settings.label_feedback.setText(str(e))
            self.ui_window_settings.label_feedback.setToolTip(str(e))

    def check_inputs(self, success_func, *inputs):
        for input in inputs:
            base_style = 'font-style: italic; background-color: white; '
            if not input.text():
                input.setStyleSheet(base_style + 'border-color: #f54021')
            else:
                input.setStyleSheet(base_style + 'border-color: #000')
        if all(input.text() for input in inputs):
            success_func()

    def toggle_password_visibility(self, is_checked):
        mode = (QLineEdit.EchoMode.Normal if is_checked 
                else QLineEdit.EchoMode.Password)
        self.ui_window.input_password.setEchoMode(mode)
            
    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui_window.input_password.text())

    def generate_and_insert_password(self):
        generated_password = self.generator.generate()
        self.ui_window.input_password.setText(generated_password)
     
    def show_invalid_input(self, input):
        original_ss = input.styleSheet()
        black = 'border: 1px solid #000;'
        red = 'border: 1px solid #f54021;'
        invalid_ss = original_ss.replace(black, red)
        input.setStyleSheet(invalid_ss)
    
    def remove_invalid_input(self, input):
        invalid_ss = input.styleSheet()
        red = 'border: 1px solid #f54021;'
        black = 'border: 1px solid #000;'
        input.setStyleSheet(invalid_ss.replace(red, black))

    def set_feedback_message(self, label, text):
        label.setText(text)
        label.setToolTip(text)
    
    def clear_feedback(self, label):
        label.setText('')
        label.setToolTip('')
from PyQt6 import QtWidgets
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QCursor, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow

from frontend.pm_login import Ui_dialog_login
from frontend.pm_main_window import Ui_main_window
from frontend.pm_new_entry import Ui_dialog_new_entry
from frontend.pm_password_settings import Ui_password_settings
from frontend.pm_signup import Ui_dialog_signup
from frontend.pm_start import Ui_dialog_start


class PasswordManagerView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_main = None

    def setup_main_window(self):
        self.ui_main = Ui_main_window()
        self.ui_main.setupUi(self)
        self.center_window(self)

    def setup_dialog_window(self, ui):
        window = QtWidgets.QDialog()
        ui_window = ui()
        ui_window.setupUi(window)
        window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.center_window(window)
        return window, ui_window
    
    def center_window(self, window):
        point = QPoint()
        point.setX(QApplication.primaryScreen().geometry().center()
                   .x() - window.width() // 2)
        point.setY(QApplication.primaryScreen().geometry().center()
                   .y() - window.height() // 2)
        window.move(point)
    
    def setup_start_window(self):
        self.start_window, self.ui_start = self.setup_dialog_window(
            Ui_dialog_start
        )
    
    def setup_login_window(self):
        self.login_window, self.ui_login = self.setup_dialog_window(
            Ui_dialog_login
        )

    def setup_signup_window(self):
        self.signup_window, self.ui_signup = self.setup_dialog_window(
            Ui_dialog_signup
        )
    
    def setup_new_entry_window(self):
        self.new_entry_window, self.ui_new_entry = self.setup_dialog_window(
            Ui_dialog_new_entry
        )
    
    def setup_entry_window(self, s_name, login, password):
        self.edit_entry_window, self.ui_entry = self.setup_dialog_window(
            Ui_dialog_new_entry
        )
        self.ui_entry.input_service_name.setText(s_name)
        self.ui_entry.input_service_name.setReadOnly(True)
        self.ui_entry.input_login.setText(login)
        self.ui_entry.input_login.setReadOnly(True)
        self.ui_entry.input_password.setText(password)
    
    def setup_password_settings_window(self, config):
        window, ui_window = self.setup_dialog_window(
            Ui_password_settings
        )
        self.password_settings_window = window
        self.ui_settings = ui_window

        self.ui_settings.spinbox_length.setValue(config['length'])
        self.ui_settings.checkbox_lcase.setChecked(config['use_lowercase'])
        self.ui_settings.checkbox_upcase.setChecked(config['use_uppercase'])
        self.ui_settings.checkbox_digits.setChecked(config['use_digits'])
        self.ui_settings.checkbox_symbols.setChecked(config['use_special_symbols'])
        self.ui_settings.input_custom.setText(config['custom_symbols'])
    
    def view_entries(self, entries, show_cb, delete_cb):
        self.ui_main.table_entries.setRowCount(0)
        for row_num, (id, service_name, login) in enumerate(entries):
            self.ui_main.table_entries.insertRow(row_num)
            self.ui_main.table_entries.setItem(
                row_num, 0, QtWidgets.QTableWidgetItem(service_name))
            self.ui_main.table_entries.setItem(
                row_num, 1, QtWidgets.QTableWidgetItem(login))

            def create_show_handler(s_name, lgn, entry_id):
                return lambda: show_cb(s_name, lgn, entry_id)

            edit_entry = QtWidgets.QPushButton('Просмотр')
            edit_entry.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            edit_entry.clicked.connect(create_show_handler(service_name, login, id))
            self.ui_main.table_entries.setCellWidget(row_num, 2, edit_entry)
        
            def create_delete_handler(entry_id):
                return lambda: delete_cb(entry_id)

            delete_entry_button = QtWidgets.QPushButton('Удалить')
            delete_entry_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            delete_entry_button.clicked.connect(create_delete_handler(id))
            self.ui_main.table_entries.setCellWidget(row_num, 3, delete_entry_button)

    def set_input_text(self, input, text):
        input.setText(text)

    def show_invalid_input(self, input, label, text):
        self.show_red_frame(input)
        self.set_feedback_message(label, text)
    
    def remove_invalid_input(self, input, label):
        self.remove_red_frame(input)
        self.clear_feedback(label)

    def show_red_frame(self, input):
        original_ss = input.styleSheet()
        original_border = 'border-color: rgb(82, 135, 169);'
        red = 'border-color: #f54021;'
        invalid_ss = original_ss.replace(original_border, red)
        input.setStyleSheet(invalid_ss)
    
    def remove_red_frame(self, input):
        invalid_ss = input.styleSheet()
        red = 'border-color: #f54021;'
        original_border = 'border-color: rgb(82, 135, 169);'
        input.setStyleSheet(invalid_ss.replace(red, original_border))

    def set_feedback_message(self, label, text):
        label.setText(text)
        label.setToolTip(text)
    
    def clear_feedback(self, label):
        label.setText('')
        label.setToolTip('')

    def hide_password(self, input):
        input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def show_password(self, input):
        input.setEchoMode(QLineEdit.EchoMode.Normal)
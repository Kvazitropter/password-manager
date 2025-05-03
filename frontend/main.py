import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import res_rc
from pm_add_new_entry import Ui_dialog_add_new_entry
from pm_create_new_storage import Ui_dialog_create_new_storage
from pm_login import Ui_dialog_login
from pm_main_window import Ui_main_window
from pm_start import Ui_dialog_start
from PyQt6 import QtWidgets


from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit

from backend.controller import Controller
from backend.custom_errors import (
    ExistingAccount,
    ExistingEntry,
    NonExistingAccount,
)
from backend.repository import Repository
from scripts.generate_password import PasswordGenerator


class PasswordManager(QMainWindow):
    def __init__(self, controller, generator):
        super(PasswordManager, self).__init__()
        self.setup_main_window(Ui_dialog_start)

        self.controller = controller
        self.generator = generator
        
        self.ui.btn_login.clicked.connect(self.open_login_window)
        self.ui.btn_create_new_storage.clicked.connect(self.open_create_new_storage_window)
        
    def setup_main_window(self, ui):
        self.ui = ui()
        self.ui.setupUi(self)
        self.center_window(self)
        
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

    def open_login_window(self):
        self.login_window = self.setup_dialog_window(Ui_dialog_login)
        self.login_window.show()
        self.ui_window.btn_submit_master_key.clicked.connect(self.login)

    def open_create_new_storage_window(self):
        self.create_new_storage_window = self.setup_dialog_window(
            Ui_dialog_create_new_storage
        )
        self.create_new_storage_window.show()
        self.ui_window.btn_submit_new_master_key.clicked.connect(self.create_new_storage)

    def open_main_window(self):
        self.setup_main_window(Ui_main_window)
        self.view_entries()
        self.ui.btn_add_new_entry.clicked.connect(self.open_add_new_entry_window)
    
    def open_add_new_entry_window(self):
        self.add_new_entry_window = self.setup_dialog_window(
            Ui_dialog_add_new_entry
        )
        self.add_new_entry_window.show()

        self.ui_window.btn_generate_password.clicked.connect(self.generate_and_insert_password)
        self.ui_window.btn_submit_entry.clicked.connect(self.add_new_entry)

        self.ui_window.btn_show.clicked.connect(self.toggle_password_visibility)
        self.ui_window.btn_copy.clicked.connect(self.copy_password)

    def open_edit_entry_window(self, service_name, login, id):
        self.edit_entry_window = self.setup_dialog_window(
            Ui_dialog_add_new_entry
        )
        password = self.controller.get_entry_password(id, self.master_key)
        self.ui_window.input_service_name.setText(service_name)
        self.ui_window.input_service_name.setReadOnly(True)
        self.ui_window.input_login.setText(login)
        self.ui_window.input_login.setReadOnly(True)
        self.ui_window.input_password.setText(password)
        self.edit_entry_window.show()

        self.ui_window.btn_generate_password.clicked.connect(self.generate_and_insert_password)
        self.ui_window.btn_submit_entry.clicked.connect(lambda: self.edit_entry(id))

        self.ui_window.btn_show.clicked.connect(self.toggle_password_visibility)
        self.ui_window.btn_copy.clicked.connect(self.copy_password)

    def toggle_password_visibility(self, is_checked):
        mode = QLineEdit.EchoMode.Normal if is_checked else QLineEdit.EchoMode.Password
        self.ui_window.input_password.setEchoMode(mode)
            
    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.ui_window.input_password.text())

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
            self.ui_window.label_feedback_login.setText(str(e))
            self.ui_window.label_feedback_login.setToolTip(str(e))
        except Exception as e:
            self.ui_window.label_feedback_master_key.setText(str(e))
            self.ui_window.label_feedback_master_key.setToolTip(str(e))

    def create_new_storage(self):
        new_login = self.ui_window.input_new_login.text()
        new_master_key = self.ui_window.input_new_master_key.text()

        try:
            self.controller.create_new_account(new_login, new_master_key)
            self.master_key = new_master_key
            self.user_login = new_login
            self.create_new_storage_window.close()
            self.open_main_window()
        except ExistingAccount as e:
            self.ui_window.label_feedback_login.setText(str(e))
            self.ui_window.label_feedback_login.setToolTip(str(e))
        except Exception as e:
            self.ui_window.label_feedback_master_key.setText(str(e))
            self.ui_window.label_feedback_master_key.setToolTip(str(e))

    def add_new_entry(self):
        service_name = self.ui_window.input_service_name.text()
        login = self.ui_window.input_login.text()
        password = self.ui_window.input_password.text()
        
        try:
            controller.add_new_entry(
                self.user_login, self.master_key, service_name, login, password
            )
            self.view_entries()
            self.add_new_entry_window.close()
        except ExistingEntry as e:
            self.ui_window.label_feedback_service_name.setText(str(e))
            self.ui_window.label_feedback_service_name.setToolTip(str(e))
            self.ui_window.label_feedback_login.setText(str(e))
            self.ui_window.label_feedback_login.setToolTip(str(e))
        except Exception as e:
            self.ui_window.label_feedback_password.setText(str(e))
            self.ui_window.label_feedback_password.setToolTip(str(e))

    def generate_and_insert_password(self):
        generated_password = self.generator.generate()
        self.ui_window.input_password.setText(generated_password)        

    def view_entries(self):
        self.ui.table_entries.setRowCount(0)  
        entries = controller.get_entries(self.user_login)
        for row_num, (id, service_name, login) in enumerate(entries):
            self.ui.table_entries.insertRow(row_num)
            self.ui.table_entries.setItem(
                row_num, 0, QtWidgets.QTableWidgetItem(service_name))
            self.ui.table_entries.setItem(
                row_num, 1, QtWidgets.QTableWidgetItem(login))

            edit_entry = QtWidgets.QPushButton('Показать')
            edit_entry.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            edit_entry.clicked.connect(
                lambda: self.open_edit_entry_window(service_name, login, id)
            )
            self.ui.table_entries.setCellWidget(row_num, 2, edit_entry)

            delete_entry_button = QtWidgets.QPushButton('Удалить')
            delete_entry_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            delete_entry_button.clicked.connect(lambda: self.delete_entry(id))
            self.ui.table_entries.setCellWidget(row_num, 3, delete_entry_button)

    def edit_entry(self, id):
        new_password = self.ui_window.input_password.text()

        try:
            controller.update_entry(self.master_key, id, new_password)
            self.view_entries()
            self.edit_entry_window.close()
        except Exception as e:
            self.ui_window.label_feedback.setText(str(e))
            self.ui_window.label_feedback.setToolTip(str(e))
    
    def delete_entry(self, id):
        self.controller.delete_entry(id)
        self.view_entries()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    res_rc.qInitResources()

    controller = Controller(Repository())
    generator = PasswordGenerator()

    window = PasswordManager(controller, generator)
    window.show()
    
    sys.exit(app.exec())

import sys

# from backend import controller
# from scripts import generator

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from pm_start import Ui_dialog_start
from pm_login import Ui_dialog_login
from pm_create_new_storage import Ui_dialog_create_new_storage
from pm_main_window import Ui_main_window
from pm_add_new_entry import Ui_dialog_add_new_entry


class PasswordManager(QMainWindow):
    def __init__(self):
        super(PasswordManager, self).__init__()
        self.ui = Ui_dialog_start()
        self.ui.setupUi(self)
        
        self.ui.btn_login.clicked.connect(self.open_login_window)
        self.ui.btn_create_new_storage.clicked.connect(self.open_create_new_storage_window)


    def open_login_window(self):
        self.login_window = QtWidgets.QDialog()
        self.ui_window = Ui_dialog_login()
        self.ui_window.setupUi(self.login_window)
        self.login_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.login_window.show()

        self.ui_window.btn_submit_master_key.clicked.connect(self.login)


    def open_create_new_storage_window(self):
        self.create_new_storage_window = QtWidgets.QDialog()
        self.ui_window = Ui_dialog_create_new_storage()
        self.ui_window.setupUi(self.create_new_storage_window)
        self.create_new_storage_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.create_new_storage_window.show()

        self.ui_window.btn_submit_new_master_key.clicked.connect(self.create_new_storage)


    def open_main_window(self):
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        self.view_entries()
        point = QPoint()
        point.setX(QApplication.primaryScreen().geometry().center().x() - self.width() // 2)
        point.setY(QApplication.primaryScreen().geometry().center().y() - self.height() // 2)
        self.move(point)
        
        self.ui.btn_add_new_entry.clicked.connect(self.open_add_new_entry_window)
    
    
    def open_add_new_entry_window(self):
        self.add_new_entry_window = QtWidgets.QDialog()
        self.ui_window = Ui_dialog_add_new_entry()
        self.ui_window.setupUi(self.add_new_entry_window)
        self.add_new_entry_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.add_new_entry_window.show()

        self.ui_window.btn_generate_password.clicked.connect(self.generate_and_insert_password)
        self.ui_window.btn_submit_entry.clicked.connect(self.add_new_entry)


    def login(self):
        master_key = self.ui_window.input_master_key.text()
        
        # is_valid_master_key = controller.has_account(master_key)
        is_valid_master_key = True
        
        if is_valid_master_key:
            self.master_key = master_key
            self.login_window.close()
            self.open_main_window()
        # else:
            # Фидбек пользователю что пароль неправильный


    def create_new_storage(self):
        new_master_key = self.ui_window.input_new_master_key.text()
        
        # is_created_new_account = controller.add_new_account(new_master_key)
        is_created_new_account = True
        
        if is_created_new_account:
            self.master_key = new_master_key
            self.create_new_storage_window.close()
            self.open_main_window()
        # else:
            # Фидбек пользователю о неудачной попытке создать новый аккаунт
    
    
    def add_new_entry(self):
        service_name = self.ui_window.input_service_name.text()
        login = self.ui_window.input_login.text()
        password = self.ui_window.input_password.text()
        
        # is_created_new_entry = controller.add_new_entry(self.master_key, service_name, login, password)
        is_created_new_entry = True
        
        if is_created_new_entry:
            self.view_entries()
            self.add_new_entry_window.close()
        # else:
            # Фидбек пользователю о неудачной попытке добавить новую запись


    def generate_and_insert_password(self):
        # generated_password = generator.generate_password()
        generated_password = "random_password"
        self.ui_window.input_password.setText(generated_password)        


    def view_entries(self):
        # entries = controller.fetch_entries(self.master_key)
        entries = [
            { 'master_key': '111', 'service_name': 'website', 'login': 'meow', 'password': 'encrypted_password' }
        ]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()

    # controller.main()
    
    sys.exit(app.exec())

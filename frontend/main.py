import sys

# from backend import controller

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
# from PyQt6.QtSql import QSqlTableModel

from pm_start import Ui_dialog_start
from pm_login import Ui_dialog_login
from pm_create_new_storage import Ui_dialog_create_new_storage
# from pm_main_window import Ui_main_window


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
        self.login_window.show()
        sender = self.sender()
        if sender.text() == "Войти в Менеджер Паролей":
            self.ui_window.btn_login.clicked.connect(self.login)


    def login(self):
        master_key = self.login_window.input_master_key.text()
        
        # controller.login_query(master_key)
        
        self.login_window.close()
    
    
    def open_create_new_storage_window(self):
        self.create_new_storage_window = QtWidgets.QDialog()
        self.ui_window = Ui_dialog_create_new_storage()
        self.ui_window.setupUi(self.create_new_storage_window)
        self.create_new_storage_window.show()
        sender = self.sender()
        if sender.text() == "Создать новое хранилище":
            self.ui_window.btn_create_new_storage.clicked.connect(self.create_new_storage)
    
    
    def create_new_storage(self):
        master_key = self.login_window.input_master_key.text()
        
        # controller.login_query(master_key)
        
        self.login_window.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()

    # controller.main()
    
    sys.exit(app.exec())

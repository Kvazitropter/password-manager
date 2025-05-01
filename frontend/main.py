import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pm_add_new_entry import Ui_dialog_add_new_entry
from pm_create_new_storage import Ui_dialog_create_new_storage
from pm_login import Ui_dialog_login
from pm_main_window import Ui_main_window
from pm_start import Ui_dialog_start
from PyQt6 import QtWidgets
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow

from backend.controller import Main as DBController

import res_rc


class PasswordManager(QMainWindow):
    def __init__(self, controller):
        super(PasswordManager, self).__init__()
        self.ui = Ui_dialog_start()
        self.ui.setupUi(self)
        
        self.controller = controller
        
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
        user_login = self.ui_window.input_login.text()
    
        is_valid_master_key = self.controller.has_master_key(master_key)
        is_valid_login = self.controller.has_login(user_login)
        
        if is_valid_master_key and is_valid_login:
            self.ui_window.label_feedback_master_key.setText('')
            self.ui_window.label_feedback_login.setText('')
            self.master_key = master_key
            self.user_login = user_login
            self.login_window.close()
            self.open_main_window()
        else:
            if not is_valid_master_key:
                # Фидбек пользователю что пароль неправильный
                self.ui_window.label_feedback_master_key.setText(
                    'Данный мастер ключ не найден. Повторите попытку'
                    )
                self.ui_window.input_master_key.setText('')
            if not is_valid_login:
                self.ui_window.label_feedback_login.setText(
                    'Данный логин не найден. Повторите попытку'
                    )
                self.ui_window.input_login.setText('')
                
        # try:
            # функция входа?
        # except ошибкаНеНайденЛогин as e:
        # except ошибкаНеверныйМастер as e:
        # или вообще не обрабатывать отдельно
        # просто исключение общая ошибка входа        

    def create_new_storage(self):
        new_master_key = self.ui_window.input_new_master_key.text()
        new_login = self.ui_window.input_new_login.text()
        
        try:
            self.controller.create_new_account(new_master_key, new_login)
            self.master_key = new_master_key
            self.user_login = new_login
            self.create_new_storage_window.close()
            self.open_main_window()
        except Exception as e:
            # Фидбек пользователю что пароль неправильный
            self.ui_window.label_feedback_master_key.setText(str(e))
        # except ошибкаЛогинУжеСущесвует as e:
           # self.ui_window.label_feedback_login.setText(str(e))
        #  либо просто одна общая ошибка регистрации

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
        # self.ui.table_entries.setRowCount(0)      
        # entries = controller.fetch_entries(self.master_key)
        for row_num, (site_name, site_login, password) in enumerate(entries):  # passwd, salt
            self.ui.table_entries.insertRow(row_num)
            self.ui.table_entries.setItem(
                row_num, 0, QtWidgets.QTableWidgetItem(site_name)
                )
            self.ui.table_entries.setItem(
                row_num, 1, QtWidgets.QTableWidgetItem(site_login)
                )

            show_paswd = QtWidgets.QPushButton('Показать')
            show_paswd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            show_paswd.clicked.connect(
                lambda _, passwd=password: self.show_password(passwd)
                )  # , salt
            self.ui.table_entries.setCellWidget(row_num, 2, show_paswd)

            delete_entry_button = QtWidgets.QPushButton('Удалить')
            delete_entry_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            delete_entry_button.clicked.connect(self.delete_entry)
            self.ui.table_entries.setCellWidget(row_num, 3, delete_entry_button)

    def show_password(self, password):  # salt
        # controller.get_decrypted(self.master_key, passwd, salt)
        passwd_window = QtWidgets.QDialog()
        passwd_line = QtWidgets.QLineEdit()
        passwd_line.setText(password)
        passwd_line.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        passwd_line.setReadOnly(True)
        layout = QtWidgets.QHBoxLayout(passwd_window)
        copy = QtWidgets.QToolButton()
        copy.setIcon(QIcon('frontend/images/copy.png'))
        copy.clicked.connect(
            lambda: QApplication.clipboard().setText(passwd_line.text())
            )
        show = QtWidgets.QToolButton()
        show.setIcon(QIcon('frontend/images/show.png'))
        show.clicked.connect(lambda: passwd_line.setEchoMode(
                                QtWidgets.QLineEdit.EchoMode.Normal if 
                                passwd_line.echoMode() ==
                                QtWidgets.QLineEdit.EchoMode.Password 
                                else QtWidgets.QLineEdit.EchoMode.Password
                            ))
        layout.addWidget(passwd_line)
        layout.addWidget(show)
        layout.addWidget(copy)
        passwd_window.exec()
 
    def delete_entry(self):
        button = self.sender()
        if button:
            row = self.ui.table_entries.indexAt(button.pos()).row()
            self.ui.table_entries.removeRow(row)
            # так же удаляем из бд


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordManager(DBController())
    window.show()
    
    sys.exit(app.exec())

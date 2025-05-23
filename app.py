import sys

from PyQt6.QtWidgets import QApplication

from backend.controller import Controller
from backend.repository import Repository
from frontend import res_rc
from frontend.main import PasswordManager
from frontend.view import PasswordManagerView
from scripts.generate_password import PasswordGenerator

if __name__ == '__main__':
    app = QApplication(sys.argv)
    res_rc.qInitResources()

    controller = Controller(Repository())
    generator = PasswordGenerator()

    view = PasswordManagerView()
    window = PasswordManager(controller, generator, view)
    window.show()
    
    sys.exit(app.exec())

import src.file_data_manager as FDM
from PyQt6.QtWidgets import QMainWindow
from src.UI.log_in_ui import Ui_LoginWindow


class LoginWindow(QMainWindow):
    def __init__(self, parent):
        super(LoginWindow, self).__init__(parent=parent)
        self.parent = parent
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        if parent._AssistantApplication__usersManager.is_any_registered():
            for i, user in enumerate(parent._AssistantApplication__usersManager.get_users_info()):
                self.ui.comboBox.addItem(f"{i + 1} - {user.split()[0]}")
        self.ui.pushButton.clicked.connect(self.login)

    def login(self):
        user_num = int(self.ui.comboBox.currentText().split(" - ")[0].strip())
        self.parent.login(user_num)
        self.close()



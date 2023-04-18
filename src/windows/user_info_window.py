import src.file_data_manager as FDM
from PyQt6.QtWidgets import QMainWindow, QLabel
from src.UI.user_info_ui import Ui_User_Info_Window


class UserInfoWindow(QMainWindow):
    def __init__(self, parent):
        super(UserInfoWindow, self).__init__(parent=parent)
        self.parent = parent
        self.ui = Ui_User_Info_Window()
        self.ui.setupUi(self)

    def send_user_info(self, user_num):
        if self.parent._AssistantApplication__usersManager.is_any_registered():
            name, age, keyword = self.parent._AssistantApplication__usersManager.get_user_info(user_num)
            self.info = QLabel(self.ui.frame_10)
            self.info.setText(f"{name}\n{age}\n{keyword}")
            self.ui.frame_10.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "font: 87 12pt \"Source Serif Pro Black\";")
        else:
            info_error = QLabel(self.ui.frame_10).setText("Нет зарегистрированных пользователей")


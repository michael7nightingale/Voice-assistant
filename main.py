import sys
import time
import os
from assistant import Assistant
from ui import Ui_MainWindow
from reg_ui import Ui_Reg_Window
from log_in_ui import Ui_LoginWindow
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import file_data_manager as FDM
from observer import Observer
from PyQt6.QtCore import *


class AssistantApplication(QMainWindow, Observer):
    """Класс приложения. Отвечает за логику отображения окна, изменения состояния
    виджетов, за создание и выключение потоков и запуск голосового помощника"""
    MAX_PHRASES_QUANTITY = 4    # максимальное количество отображаемых фраз

    def __init__(self, parent=None):
        super(AssistantApplication, self).__init__(parent)  # инициализатор QMainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)   # установка виджетов
        self.sidebarConditions = [self.ui.sidebarClosedSize, self.ui.sidebarOpenedSize]
        self.sidebarOpened = False  # состояние сайдбара
        # Ассистент
        self.assist_condition = False
        self.assistant = Assistant()
        self.assistant.subscribe(self)
        # Потоки
        self.assistThread_instance = AssistantThread(self)
        self.popupThread_instance = PopupThread(self)
        # Окна
        self.regwindow = RegWindow(self)
        self.dlg = QMainWindow(self)
        self.login_window = LoginWindow(self)
        # Log in / Log up
        self.check_registration()
        # Первоначальная очистка окон
        self.clear_messages()
        self._button_checker()

    def check_registration(self):
        """Если есть зарегистрированные пользователи, открываем окно входа,
        если нет, то окно регистрации"""
        if FDM.is_any_registrated():
            self.show_login_window()
        else:
            self.show_regwindow()

    def _button_checker(self):
        """Контроль кнопок"""
        self.ui.button_open_sidebar.clicked.connect(self.changeSidebarCondition)
        self.ui.button_start.clicked.connect(self.changeAssistantCondition)
        self.ui.button_exit.clicked.connect(lambda: exit())
        self.ui.my_account.clicked.connect(self.send_user_info)
        self.ui.change_account.clicked.connect(self.show_login_window)
        self.ui.button_clear_messages.clicked.connect(self.clear_messages)
        self.ui.button_commands.clicked.connect(self.show_regwindow)

    def clear_messages(self):
        """Убрать все рамки сообщений"""
        for i in range(1, 100):
            if hasattr(self.ui, f"frameMessages{i}"):
                self.ui.__dict__[f"frameMessages{i}"].hide()
            else:
                break
        self.assistant.phrases.clear()

    def changeSidebarCondition(self):
        """Закрытие и открытие сайдбара"""
        self.sidebarOpened = not self.sidebarOpened
        self.ui.sidebar.setMaximumSize(self.sidebarConditions[int(self.sidebarOpened)])

    def changeAssistantCondition(self):
        """Запуск и выключение помощника"""
        self.assist_condition = not self.assist_condition
        if self.assist_condition:
            self.assistThread_instance.start()
        else:
            self.assistant.source.stream = None
            if os.path.exists("response.mp3"):
                os.remove("response.mp3")
            self.assistThread_instance.terminate()

    def update(self, data: list[tuple[str, str]]) -> None:      # !!!!!!!ВЫНЕСТИ В ОТДTЛЬНЫЙ СЕТАП И КЛАСССС!!!!!!!!!!
        """Переопределение метода класса Наблюдатель"""
        if len(data) > self.MAX_PHRASES_QUANTITY:
            data = data[-self.MAX_PHRASES_QUANTITY:]
        for idx, dataText in enumerate(data[::-1]):
            self.ui.__dict__[f"frameMessages{idx + 1}"].show()
            self.ui.__dict__[f"message{idx + 1}"].setText(dataText[1])
            self.ui.__dict__[f"fromwho{idx + 1}"].setText(dataText[0])
        time.sleep(0.3)

    def send_user_info(self):
        self.dlg.setMinimumSize(QSize(300, 200))
        self.dlg.resize(0, 0)
        self.dlg.setWindowTitle("Пользователь")
        self.dlg.setWindowIcon(QIcon("icons/logo/circle-user.png"))
        self.frame_10 = QFrame(self.dlg)
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.dlg.setCentralWidget(self.frame_10)
        if FDM.is_any_registrated():
            name, age, keyword = FDM.get_user_info(self.assistant.user_num)
            self.info = QLabel(self.frame_10)
            self.info.setText(f"{name}\n{age}\n{keyword}")
            self.frame_10.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "font: 87 12pt \"Source Serif Pro Black\";")
        else:
            info_error = QLabel(self.frame_10).setText("Нет зарегистрированных пользователей")
        self.dlg.show()

    def show_regwindow(self):
        self.regwindow.show()

    def new_user(self, name, age, keyword):
        FDM.save_information(name, age, keyword)
        self.assistThread_instance.terminate()
        self.assistant.user_num = FDM.amount_of_users

    def show_login_window(self):
        self.login_window.show()

    def login(self, user_num):
        self.assistThread_instance.terminate()
        self.assistant.user_num = user_num


class AssistantThread(QThread):
    """Поток для помощника. Разделение на потоки предотвращает зависание
    главного окна и оптимизирует работу программы"""
    def __init__(self, application, parent=None):
        super(AssistantThread, self).__init__(parent)
        self.application = application

    def run(self):
        """Переопределение абстрактного метода run"""
        if self.application.assist_condition:
            self.application.assistant.execute()


class PopupThread(QThread):
    """Поток для окон сообщения"""
    def __init__(self, application, parent=None):
        super(PopupThread, self).__init__(parent)
        # на какое окно влиять
        self.application = application

    def run(self):
        self.application.button_clicked()


class RegWindow(QMainWindow):
    """Окно регистрации"""
    def __init__(self, parent):
        super(RegWindow, self).__init__(parent=parent)
        self.parent = parent
        self.ui = Ui_Reg_Window()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send_input_data)

    def send_input_data(self) -> None:
        name = self.ui.lineEdit.text()
        age = self.ui.lineEdit_2.text()
        keyword = self.ui.lineEdit_3.text()
        if self.validDate(phrase=name) and self.validAge(phrase=age) and self.validDate(phrase=keyword):
            self.parent.new_user(name, age, keyword)
            self.close()

    def validDate(self, phrase: str, type_: type = str,  maxQuantityWords: int = 3, maxLength: int = 40):
        """Проверка слов"""
        if phrase is not None:
            divided_phrase = phrase.split()
            return all(i.isalpha() for i in divided_phrase)
        else:
            return False

    def validAge(self, phrase: str) -> bool:
        """Проверка возраста"""
        if phrase.isdigit():
            if 9 <= int(phrase) <= 100:
                return True
        return False


class LoginWindow(QMainWindow):
    def __init__(self, parent):
        super(LoginWindow, self).__init__(parent=parent)
        self.parent = parent
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        if FDM.is_any_registrated():
            for i, user in enumerate(FDM.get_users_info()):
                self.ui.comboBox.addItem(f"{i + 1} - {user.split()[0]}")
        self.ui.pushButton.clicked.connect(self.login)

    def login(self):
        user_num = int(self.ui.comboBox.currentText().split(" - ")[0].strip())
        self.parent.login(user_num)
        self.close()


if __name__ == '__main__':
    """Непосредственно запуск приложения"""
    app = QApplication(sys.argv)
    assistantAppGUI = AssistantApplication()
    assistantAppGUI.show()
    app.exec()




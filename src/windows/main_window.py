import time
import os
from src.assistant import Assistant
from src.UI.ui import Ui_MainWindow
from src.windows import (reg_window,
                        login_window,
                        user_info_window)
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import src.file_data_manager as FDM
from src.observer import Observer
from PyQt6.QtCore import *



class AssistantApplication(QMainWindow, Observer, FDM.DataMixin):
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
        self.reg_window = reg_window.RegWindow(self)
        self.login_window = login_window.LoginWindow(self)
        self.user_info_window = user_info_window.UserInfoWindow(self)
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
            self.show_reg_window()

    def _button_checker(self):
        """Контроль кнопок"""
        self.ui.button_open_sidebar.clicked.connect(self.changeSidebarCondition)
        self.ui.button_start.clicked.connect(self.changeAssistantCondition)
        self.ui.button_exit.clicked.connect(lambda: exit())
        self.ui.my_account.clicked.connect(self.show_user_info_window)
        self.ui.change_account.clicked.connect(self.show_login_window)
        self.ui.button_clear_messages.clicked.connect(self.clear_messages)
        self.ui.button_commands.clicked.connect(self.show_reg_window)

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

    def update(self, data: list[tuple[str, str]]) -> None:
        """Переопределение метода класса Наблюдатель"""
        if len(data) > self.MAX_PHRASES_QUANTITY:
            data = data[-self.MAX_PHRASES_QUANTITY:]
        for idx, dataText in enumerate(data[::-1]):
            self.ui.__dict__[f"frameMessages{idx + 1}"].show()
            self.ui.__dict__[f"message{idx + 1}"].setText(dataText[1])
            self.ui.__dict__[f"fromwho{idx + 1}"].setText(dataText[0])
        time.sleep(0.3)

    def show_user_info_window(self):
        self.user_info_window.send_user_info(self.assistant.user_num)
        self.user_info_window.show()

    def show_reg_window(self):
        """Открытие окна регистрации"""
        self.reg_window.show()

    def new_user(self, name, age, keyword):
        FDM.save_information(name, age, keyword)
        self.login(FDM.amount_of_users)

    def show_login_window(self):
        """Открытие окна входа"""
        self.login_window.show()

    def login(self, user_num):
        """Вход в аккаунт"""
        self.assistThread_instance.terminate()
        self.assist_condition = False
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


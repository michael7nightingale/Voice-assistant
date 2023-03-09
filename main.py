import sys
import time
from assistant import Assistant
from assistapp import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication
from observer import Observer
from PyQt6.QtCore import *


class AssistantApplication(QMainWindow, Observer):
    """Класс приложения. Отвечает за логику отображения окна, изменения состояния
    виджетов, за создание и выключение потоков и запуск голосового помощника"""
    MAX_PHRASES_QUANTITY = 4    # максимальное количество отображаемых фраз

    def __init__(self, parent=None):
        super(AssistantApplication, self).__init__(parent)  # инициализатор QMainWindow
        self.assist_condition = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)   # установка виджетов
        self.sidebarConditions = [self.ui.sidebarClosedSize, self.ui.sidebarOpenedSize]
        self.sidebarOpened = False  # состояние сайдбара
        self.assistant = Assistant()
        self.assistant.subscribe(self)
        self.assistThread_instance = AssistantThread(self)
        self._button_checker()

    def _button_checker(self):
        self.ui.sidebarOpen.clicked.connect(self.changeSidebarCondition)
        self.ui.startButton.clicked.connect(self.changeAssistantCondition)
        self.ui.exitbutton.clicked.connect(lambda: exit())

    def changeSidebarCondition(self):
        """Закрытие и открытие сайдбара"""
        self.sidebarOpened = not self.sidebarOpened
        self.ui.sidebar.setMaximumSize(self.sidebarConditions[int(self.sidebarOpened)])

    def changeAssistantCondition(self):
        """Запуск и выключение помощника"""
        self.assist_condition = not self.assist_condition
        if self.assist_condition:
            self.assistThread_instance.start()
            self.ui.startButton.setText("Stop")
        else:
            self.assistThread_instance.terminate()
            self.ui.startButton.setText("Start")


    def update(self, data: list[tuple[str, str]]) -> None:
        """Переопределение метода класса Наблюдатель"""
        if len(data) > self.MAX_PHRASES_QUANTITY:
            data = data[-self.MAX_PHRASES_QUANTITY:]
        for idx, dataText in enumerate(data[::-1]):
            self.ui.__dict__[f"frameMessages{idx + 1}"].show()
            self.ui.__dict__[f"message{idx + 1}"].setText(dataText[1])
            self.ui.__dict__[f"fromwho{idx + 1}"].setText(dataText[0])
        time.sleep(0.3)


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


if __name__ == '__main__':
    """Непосредственно запуск приложения"""
    app = QApplication(sys.argv)
    assistantAppGUI = AssistantApplication()
    assistantAppGUI.show()
    app.exec()


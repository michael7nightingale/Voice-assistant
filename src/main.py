import sys
from src.windows import main_window
from PyQt6.QtWidgets import QApplication


def run_app():
    app = QApplication(sys.argv)
    assistantAppGUI = main_window.AssistantApplication()
    assistantAppGUI.show()
    app.exec()


if __name__ == '__main__':
    """Непосредственно запуск приложения"""
    run_app()



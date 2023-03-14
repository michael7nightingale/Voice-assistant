import src.file_data_manager as FDM
from PyQt6.QtWidgets import QMainWindow
from src.UI.reg_ui import Ui_Reg_Window


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

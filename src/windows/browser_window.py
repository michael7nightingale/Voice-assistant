from PyQt6.QtWidgets import QMainWindow, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView


class BrowserWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BrowserWindow, self).__init__(parent=parent)

        self.setupUI()

    def setupUI(self):
        self.browser = QWebEngineView()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.browser)
        self.setLayout(self.vbox)
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle("Assistant browser")

    def load_page(self, html):
        self.browser.setHtml(html)



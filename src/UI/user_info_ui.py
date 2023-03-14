from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_User_Info_Window(object):
    def setupUi(self, Ui_User_Info_Window):
        Ui_User_Info_Window.setObjectName("Reg_Window")
        Ui_User_Info_Window.resize(585, 462)
        Ui_User_Info_Window.setMaximumSize(QtCore.QSize(585, 462))
        Ui_User_Info_Window.setStyleSheet("background-color: rgb(0, 244, 179);")
        Ui_User_Info_Window.setWindowTitle("Новый пользователь")
        Ui_User_Info_Window.setWindowIcon(QtGui.QIcon("../../icons/logo/chart-user.png"))
        Ui_User_Info_Window.setWindowTitle("Пользователь")
        Ui_User_Info_Window.setWindowIcon(QtGui.QIcon("icons/logo/circle-user.png"))
        self.frame_10 = QtWidgets.QFrame(Ui_User_Info_Window)
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        Ui_User_Info_Window.setCentralWidget(self.frame_10)
        self.statusbar = QtWidgets.QStatusBar(Ui_User_Info_Window)
        self.statusbar.setObjectName("statusbar")
        Ui_User_Info_Window.setStatusBar(self.statusbar)

        self.retranslateUi(Ui_User_Info_Window)
        QtCore.QMetaObject.connectSlotsByName(Ui_User_Info_Window)

    def retranslateUi(self, Reg_Window):
        _translate = QtCore.QCoreApplication.translate
        Reg_Window.setWindowTitle(_translate("Reg_Window", "MainWindow"))

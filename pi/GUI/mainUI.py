# -*- coding: utf-8 -*-
import PyQt6.QtCore
################################################################################
## Form generated from reading UI file 'mainUI2.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide2.QtCore import Qt

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLayout, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QScrollBar, QSizePolicy,
    QSlider, QStackedWidget, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)
import icon_rc
class ClickableLabel(QLabel):
    clicked = Signal()  # 클릭 이벤트를 위한 시그널 정의

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()  # 클릭 시그널 방출
        super().mousePressEvent(event)

class ClickableQText(QTextEdit):
    clicked = Signal()  # 클릭 이벤트를 위한 시그널 정의

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()  # 클릭 시그널 방출
        super().mousePressEvent(event)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(663, 604)
        MainWindow.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color : rgb(254, 252, 247);")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.WifiPage = QWidget()
        self.WifiPage.setObjectName(u"WifiPage")
        self.frame_12 = QFrame(self.WifiPage)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setGeometry(QRect(0, 0, 651, 541))
        self.frame_12.setStyleSheet(u"background-color : rgb(254, 252, 247);")
        self.frame_12.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_13 = QFrame(self.frame_12)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setGeometry(QRect(40, 110, 551, 351))
        self.frame_13.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_13.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(203, 203, 203);")
        self.frame_13.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_13.setLineWidth(0)
        self.verticalScrollBar_4 = QScrollBar(self.frame_13)
        self.verticalScrollBar_4.setObjectName(u"verticalScrollBar_4")
        self.verticalScrollBar_4.setGeometry(QRect(620, 170, 17, 68))
        self.verticalScrollBar_4.setStyleSheet(u"")
        self.verticalScrollBar_4.setOrientation(Qt.Orientation.Vertical)
        self.networkText1 = QLabel(self.frame_13)
        self.networkText1.setObjectName(u"networkText1")
        self.networkText1.setGeometry(QRect(10, 20, 81, 21))
        font = QFont()
        font.setPointSize(15)
        self.networkText1.setFont(font)
        self.networkText1.setStyleSheet(u"border:0px;")
        self.networkText1.setLineWidth(0)
        self.networkText1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reloadImage = QPushButton(self.frame_13)
        self.reloadImage.setObjectName(u"reloadImage")
        self.reloadImage.setGeometry(QRect(500, 10, 41, 21))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(False)
        self.reloadImage.setFont(font1)
        self.reloadImage.setStyleSheet(u"border-radius:15px;\n"
"image: url(:/icon/icon/reload.png);")
        self.scrollArea_3 = QScrollArea(self.frame_13)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setGeometry(QRect(0, 40, 541, 291))
        self.scrollArea_3.setStyleSheet(u"QScrollBar::handle:vertical{\n"
"	background-color: rgb(123,123,123);\n"
"	min-height:5px;\n"
"	border-radius:3px;\n"
"	margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"/*QScrollBar:vertical{\n"
"	border:0px;\n"
"	background-color:rgb(0, 0, 0);\n"
"	width:10px;\n"
"	border-radius:3px;\n"
"}*/\n"
"/*QScrollBar::sub-line:vertical{\n"
"	border:none;\n"
"	background-color:rgb(59, 59, 90); \n"
"	height: 15px;\n"
"	border-top-left-radius:7px;\n"
"	border-top-right-radius:7px;\n"
"}*/\n"
"QScrollBar::handle:vertical:hover{\n"
"	background-color: rgb(255,255 ,255);\n"
"}\n"
"/*QScrollBar::handle:vertical:pressed{\n"
"	background-color: rgb(183, 183, 183);\n"
"}*/")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 541, 291))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(20)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.WIFIButton = QPushButton(self.scrollAreaWidgetContents_3)
        self.WIFIButton.setObjectName(u"WIFIButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WIFIButton.sizePolicy().hasHeightForWidth())
        self.WIFIButton.setSizePolicy(sizePolicy)
        self.WIFIButton.setMinimumSize(QSize(481, 27))
        self.WIFIButton.setMaximumSize(QSize(481, 131))
        self.WIFIButton.setFont(font)
        self.WIFIButton.setStyleSheet(u"image: url(:/icon/icon/wifi_lock.png);\n"
"image-position:left;\n"
"background-color : rgb(254, 252, 247);")

        self.verticalLayout_6.addWidget(self.WIFIButton)

        self.WIFIButton1 = QPushButton(self.scrollAreaWidgetContents_3)
        self.WIFIButton1.setObjectName(u"WIFIButton1")
        sizePolicy.setHeightForWidth(self.WIFIButton1.sizePolicy().hasHeightForWidth())
        self.WIFIButton1.setSizePolicy(sizePolicy)
        self.WIFIButton1.setMinimumSize(QSize(481, 27))
        self.WIFIButton1.setMaximumSize(QSize(481, 131))
        self.WIFIButton1.setFont(font)
        self.WIFIButton1.setStyleSheet(u"image: url(:/icon/icon/wifi_lock.png);\n"
"image-position:left;\n"
"background-color : rgb(254, 252, 247);")

        self.verticalLayout_6.addWidget(self.WIFIButton1)


        self.verticalLayout_5.addLayout(self.verticalLayout_6)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.networkText = QLabel(self.frame_12)
        self.networkText.setObjectName(u"networkText")
        self.networkText.setGeometry(QRect(40, 70, 181, 31))
        font2 = QFont()
        font2.setPointSize(20)
        self.networkText.setFont(font2)
        self.networkText.setStyleSheet(u"border:0px;")
        self.networkText.setLineWidth(0)
        self.networkText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logoText_0 = QLabel(self.frame_12)
        self.logoText_0.setObjectName(u"logoText_0")
        self.logoText_0.setGeometry(QRect(510, 20, 111, 51))
        self.logoText_0.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.logoImage_0 = QLabel(self.frame_12)
        self.logoImage_0.setObjectName(u"logoImage_0")
        self.logoImage_0.setGeometry(QRect(460, 10, 61, 51))
        self.logoImage_0.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.stackedWidget.addWidget(self.WifiPage)
        self.PasswordPage = QWidget()
        self.PasswordPage.setObjectName(u"PasswordPage")
        self.frame_9 = QFrame(self.PasswordPage)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setGeometry(QRect(0, 0, 651, 541))
        self.frame_9.setStyleSheet(u"background-color : rgb(254, 252, 247);")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.pwdInput = QFrame(self.frame_9)
        self.pwdInput.setObjectName(u"pwdInput")
        self.pwdInput.setGeometry(QRect(80, 210, 451, 31))
        self.pwdInput.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pwdInput.setStyleSheet(u"border-top: 4px solid;\n"
"border-radius:15px;\n"
"background-color:rgb(203, 203, 203);\n"
"border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.pwdInput.setFrameShape(QFrame.Shape.NoFrame)
        self.pwdInput.setFrameShadow(QFrame.Shadow.Plain)
        self.pwdInput.setLineWidth(0)
        self.pwdPlacehold = QLabel(self.pwdInput)
        self.pwdPlacehold.setObjectName(u"pwdPlacehold")
        self.pwdPlacehold.setGeometry(QRect(20, 0, 251, 31))
        self.pwdPlacehold.setStyleSheet(u"border:0px;\n"
"color:rgb(121, 121, 121);\n"
"background-color:transparent;")
        self.pwdPlacehold.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pwdImage = ClickableLabel(self.pwdInput)
        self.pwdImage.setObjectName(u"pwdImage")
        self.pwdImage.setGeometry(QRect(400, 0, 51, 31))
        self.pwdImage.setStyleSheet(u"border:0px;\n"
"color:rgb(121, 121, 121);\n"
"background-color:transparent;\n"
"image: url(:/icon/icon/eye_close.png);")
        self.networkName = QLabel(self.frame_9)
        self.networkName.setObjectName(u"networkName")
        self.networkName.setGeometry(QRect(20, 30, 151, 21))
        self.networkName.setFont(font)
        self.networkName.setStyleSheet(u"border:0px;\n"
        "background-color : transparent;")
        self.networkName.setLineWidth(0)
        self.networkName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.BackButton = QPushButton(self.frame_9)
        self.BackButton.setObjectName(u"BackButton")
        self.BackButton.setGeometry(QRect(0, 30, 51, 21))
        self.BackButton.setStyleSheet(u"border:0px;\n"
"image: url(:/icon/icon/back.png);\n"
"background-color : transparent;")
        self.pwdText = QLabel(self.frame_9)
        self.pwdText.setObjectName(u"pwdText")
        self.pwdText.setGeometry(QRect(80, 180, 81, 21))
        font3 = QFont()
        font3.setPointSize(12)
        self.pwdText.setFont(font3)
        self.pwdText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.yesButton_1 = QPushButton(self.frame_9)
        self.yesButton_1.setObjectName(u"yesButton_1")
        self.yesButton_1.setGeometry(QRect(550, 500, 61, 31))
        font4 = QFont()
        font4.setPointSize(15)
        font4.setBold(False)
        self.yesButton_1.setFont(font4)
        self.yesButton_1.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.logoImage_1 = QLabel(self.frame_9)
        self.logoImage_1.setObjectName(u"logoImage_1")
        self.logoImage_1.setGeometry(QRect(460, 10, 61, 51))
        self.logoImage_1.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.logoText_1 = QLabel(self.frame_9)
        self.logoText_1.setObjectName(u"logoText_1")
        self.logoText_1.setGeometry(QRect(510, 20, 111, 51))
        self.logoText_1.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.pwdInput.raise_()
        self.networkName.raise_()
        self.pwdText.raise_()
        self.yesButton_1.raise_()
        self.logoImage_1.raise_()
        self.logoText_1.raise_()
        self.BackButton.raise_()
        self.stackedWidget.addWidget(self.PasswordPage)
        self.QRPage = QWidget()
        self.QRPage.setObjectName(u"QRPage")
        self.frame_5 = QFrame(self.QRPage)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(0, 0, 651, 541))
        self.frame_5.setStyleSheet(u"background-color : rgb(254, 252, 247);")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.nextButton_2 = QPushButton(self.frame_5)
        self.nextButton_2.setObjectName(u"nextButton_2")
        self.nextButton_2.setGeometry(QRect(550, 500, 61, 31))
        self.nextButton_2.setFont(font4)
        self.nextButton_2.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.QRText2 = QTextEdit(self.frame_5)
        self.QRText2.setObjectName(u"QRText2")
        self.QRText2.setGeometry(QRect(160, 490, 311, 61))
        self.QRText2.setStyleSheet(u"border:0px;\n"
"background-color:transparent;")
        self.QRText2.setReadOnly(True)
        self.QRText = QTextEdit(self.frame_5)
        self.QRText.setObjectName(u"QRText")
        self.QRText.setGeometry(QRect(320, 320, 291, 121))
        self.QRText.setStyleSheet(u"border:0px;")
        self.characterImage = QLabel(self.frame_5)
        self.characterImage.setObjectName(u"characterImage")
        self.characterImage.setGeometry(QRect(330, 180, 241, 131))
        self.characterImage.setStyleSheet(u"image: url(:/icon/icon/\uadf8\ub9bc_\ub315\uccad.png);")
        self.logoImage_2 = ClickableLabel(self.frame_5)
        self.logoImage_2.setObjectName(u"logoImage_2")
        self.logoImage_2.setGeometry(QRect(10, 10, 61, 51))
        self.logoImage_2.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.logoImage_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logoImage_2.setWordWrap(False)
        self.logoImage_2.setOpenExternalLinks(False)
        self.logoImage_2.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.logoText_2 = QLabel(self.frame_5)
        self.logoText_2.setObjectName(u"logoText_2")
        self.logoText_2.setGeometry(QRect(60, 20, 111, 51))
        self.logoText_2.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.QRText3 = QTextEdit(self.frame_5)
        self.QRText3.setObjectName(u"QRText3")
        self.QRText3.setGeometry(QRect(500, 460, 111, 41))
        self.QRText3.setStyleSheet(u"border:0px;\n"
"background-color:transparent;")
        self.stackedWidget.addWidget(self.QRPage)
        self.MainPage = QWidget()
        self.MainPage.setObjectName(u"MainPage")
        self.MainPage.setStyleSheet(u"background-color:rgb(254, 252, 247);")
        self.frame_3 = QFrame(self.MainPage)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(0, 0, 651, 541))
        self.frame_3.setStyleSheet(u"background-color : transparent;\n"
"")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.frame = QFrame(self.frame_3)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 651, 31))
        self.frame.setStyleSheet(u"background-color:rgb(174, 222, 211);\n"
"border:0px;")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame.setLineWidth(0)
        self.horizontalLayoutWidget = QWidget(self.frame)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 651, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(100)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.dateText_3 = QLabel(self.horizontalLayoutWidget)
        self.dateText_3.setObjectName(u"dateText_3")
        self.dateText_3.setFont(font3)
        self.dateText_3.setStyleSheet(u"margin-left:10px;")
        self.dateText_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.dateText_3)

        self.timeText_3 = QLabel(self.horizontalLayoutWidget)
        self.timeText_3.setObjectName(u"timeText_3")
        self.timeText_3.setFont(font3)
        self.timeText_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.timeText_3)

        self.label_5 = QLabel(self.horizontalLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.settingText = ClickableQText(self.frame_3)
        self.settingText.setObjectName(u"settingText")
        self.settingText.setGeometry(QRect(440, 390, 141, 61))
        font5 = QFont()
        font5.setPointSize(33)
        self.settingText.setFont(font5)
        self.settingText.setStyleSheet(u"border:0px;\n"
"background-color:transparent;")
        self.settingText.setReadOnly(True)
        self.greetings = QLabel(self.frame_3)
        self.greetings.setObjectName(u"greetings")
        self.greetings.setGeometry(QRect(30, 110, 381, 31))
        font6 = QFont()
        font6.setPointSize(18)
        self.greetings.setFont(font6)
        self.weatherImage = QLabel(self.frame_3)
        self.weatherImage.setObjectName(u"weatherImage")
        self.weatherImage.setGeometry(QRect(310, 180, 151, 121))
        self.weatherImage.setStyleSheet(u"background-color:transparent;\n"
"image: url(:/icon/icon/sunny_cloud.png);")
        self.logoImage_3 = ClickableLabel(self.frame_3)
        self.logoImage_3.setObjectName(u"logoImage_3")
        self.logoImage_3.setGeometry(QRect(470, 40, 51, 51))
        self.logoImage_3.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.logoImage_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logoImage_3.setOpenExternalLinks(True)
        self.weatherText = QTextEdit(self.frame_3)
        self.weatherText.setObjectName(u"weatherText")
        self.weatherText.setGeometry(QRect(440, 190, 151, 111))
        font7 = QFont()
        font7.setPointSize(25)
        self.weatherText.setFont(font7)
        self.weatherText.setStyleSheet(u"border:0px;\n"
"background-color:transparent;")
        self.weatherButton = QPushButton(self.frame_3)
        self.weatherButton.setObjectName(u"weatherButton")
        self.weatherButton.setGeometry(QRect(320, 170, 281, 151))
        font8 = QFont()
        font8.setPointSize(60)
        self.weatherButton.setFont(font8)
        self.weatherButton.setStyleSheet(u"border-radius:15px;\n"
"background-color:rgb(194, 226, 219);")
        self.diaryButton_3 = QPushButton(self.frame_3)
        self.diaryButton_3.setObjectName(u"diaryButton_3")
        self.diaryButton_3.setGeometry(QRect(20, 170, 281, 321))
        font9 = QFont()
        font9.setPointSize(60)
        font9.setBold(False)
        self.diaryButton_3.setFont(font9)
        self.diaryButton_3.setStyleSheet(u"border-radius:15px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.settingButton = QPushButton(self.frame_3)
        self.settingButton.setObjectName(u"settingButton")
        self.settingButton.setGeometry(QRect(320, 350, 281, 141))
        self.settingButton.setFont(font9)
        self.settingButton.setStyleSheet(u"border-radius:15px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.logoText_3 = QLabel(self.frame_3)
        self.logoText_3.setObjectName(u"logoText_3")
        self.logoText_3.setGeometry(QRect(510, 50, 111, 51))
        self.logoText_3.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.diaryImage = ClickableLabel(self.frame_3)
        self.diaryImage.setObjectName(u"diaryImage")
        self.diaryImage.setGeometry(QRect(90, 200, 131, 121))
        self.diaryImage.setStyleSheet(u"background-color:transparent;\n"
"image: url(:/icon/icon/diary1.png);")
        self.diaryText = ClickableQText(self.frame_3)
        self.diaryText.setObjectName(u"diaryText")
        self.diaryText.setGeometry(QRect(40, 320, 231, 141))
        self.diaryText.setFont(font5)
        self.diaryText.setStyleSheet(u"border:0px;\n"
"background-color:transparent;")
        self.diaryText.setReadOnly(True)
        self.settingImage = ClickableLabel(self.frame_3)
        self.settingImage.setObjectName(u"settingImage")
        self.settingImage.setGeometry(QRect(330, 350, 131, 141))
        self.settingImage.setStyleSheet(u"background-color:transparent;\n"
"image: url(:/icon/icon/setting.png);")
        self.settingButton.raise_()
        self.weatherButton.raise_()
        self.frame.raise_()
        self.settingText.raise_()
        self.greetings.raise_()
        self.weatherImage.raise_()
        self.logoImage_3.raise_()
        self.weatherText.raise_()
        self.diaryButton_3.raise_()
        self.logoText_3.raise_()
        self.diaryImage.raise_()
        self.diaryText.raise_()
        self.settingImage.raise_()
        self.stackedWidget.addWidget(self.MainPage)
        self.SettingPage = QWidget()
        self.SettingPage.setObjectName(u"SettingPage")
        self.frame_4 = QFrame(self.SettingPage)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(0, 0, 651, 541))
        self.frame_4.setStyleSheet(u"background-color : transparent;\n"
"")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2 = QFrame(self.frame_4)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 0, 651, 31))
        self.frame_2.setStyleSheet(u"background-color:rgb(174, 222, 211);\n"
"border:0px;")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2.setLineWidth(0)
        self.horizontalLayoutWidget_2 = QWidget(self.frame_2)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, 651, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setSpacing(100)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.dateText_4 = QLabel(self.horizontalLayoutWidget_2)
        self.dateText_4.setObjectName(u"dateText_4")
        self.dateText_4.setFont(font3)
        self.dateText_4.setStyleSheet(u"margin-left:10px;")
        self.dateText_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.dateText_4)

        self.timeText_4 = QLabel(self.horizontalLayoutWidget_2)
        self.timeText_4.setObjectName(u"timeText_4")
        self.timeText_4.setFont(font3)
        self.timeText_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.timeText_4)

        self.label_13 = QLabel(self.horizontalLayoutWidget_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_13)

        self.settingPageText = QLabel(self.frame_4)
        self.settingPageText.setObjectName(u"settingPageText")
        self.settingPageText.setGeometry(QRect(50, 90, 81, 61))
        font10 = QFont()
        font10.setPointSize(30)
        font10.setBold(True)
        self.settingPageText.setFont(font10)
        self.logoImage_4 = QLabel(self.frame_4)
        self.logoImage_4.setObjectName(u"logoImage_4")
        self.logoImage_4.setGeometry(QRect(470, 40, 51, 51))
        self.logoImage_4.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.infoButton = QPushButton(self.frame_4)
        self.infoButton.setObjectName(u"infoButton")
        self.infoButton.setGeometry(QRect(40, 200, 251, 201))
        self.infoButton.setFont(font9)
        self.infoButton.setStyleSheet(u"border-radius:15px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.systemButton = QPushButton(self.frame_4)
        self.systemButton.setObjectName(u"systemButton")
        self.systemButton.setGeometry(QRect(320, 200, 251, 201))
        self.systemButton.setFont(font9)
        self.systemButton.setStyleSheet(u"border-radius:15px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.logoText_4 = QLabel(self.frame_4)
        self.logoText_4.setObjectName(u"logoText_4")
        self.logoText_4.setGeometry(QRect(510, 50, 111, 51))
        self.logoText_4.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.systemImage = ClickableLabel(self.frame_4)
        self.systemImage.setObjectName(u"systemImage")
        self.systemImage.setGeometry(QRect(390, 210, 111, 121))
        self.systemImage.setStyleSheet(u"background-color:transparent;\n"
"image: url(:/icon/icon/setting.png);")
        self.infoImage = ClickableLabel(self.frame_4)
        self.infoImage.setObjectName(u"infoImage")
        self.infoImage.setGeometry(QRect(120, 210, 101, 111))
        self.infoImage.setStyleSheet(u"background-color:transparent;\n"
"image: url(:/icon/icon/pet_footprint.png);")
        self.infoText = ClickableLabel(self.frame_4)
        self.infoText.setObjectName(u"infoText")
        self.infoText.setGeometry(QRect(80, 320, 171, 71))
        self.infoText.setFont(font5)
        self.infoText.setStyleSheet(u"border:0px;\n"
"background-color:transparent;")
        self.infoText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.systemText = ClickableLabel(self.frame_4)
        self.systemText.setObjectName(u"systemText")
        self.systemText.setGeometry(QRect(360, 320, 171, 71))
        self.systemText.setFont(font5)
        self.systemText.setStyleSheet(u"border:0px;\n"
"background-color:transparent;")
        self.systemText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.systemButton.raise_()
        self.frame_2.raise_()
        self.settingPageText.raise_()
        self.logoImage_4.raise_()
        self.infoButton.raise_()
        self.logoText_4.raise_()
        self.systemImage.raise_()
        self.infoImage.raise_()
        self.infoText.raise_()
        self.systemText.raise_()
        self.cancelButton_4 = QPushButton(self.SettingPage)
        self.cancelButton_4.setObjectName(u"cancelButton_4")
        self.cancelButton_4.setGeometry(QRect(530, 500, 61, 31))
        self.cancelButton_4.setFont(font4)
        self.cancelButton_4.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.stackedWidget.addWidget(self.SettingPage)
        self.SystemPage = QWidget()
        self.SystemPage.setObjectName(u"SystemPage")
        self.frame_6 = QFrame(self.SystemPage)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(0, 0, 651, 541))
        self.frame_6.setStyleSheet(u"background-color : transparent;\n"
"")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setGeometry(QRect(0, 0, 651, 31))
        self.frame_7.setStyleSheet(u"background-color:rgb(174, 222, 211);\n"
"border:0px;")
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_7.setLineWidth(0)
        self.horizontalLayoutWidget_3 = QWidget(self.frame_7)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(0, 0, 651, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setSpacing(100)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.dateText_5 = QLabel(self.horizontalLayoutWidget_3)
        self.dateText_5.setObjectName(u"dateText_5")
        self.dateText_5.setFont(font3)
        self.dateText_5.setStyleSheet(u"margin-left:10px;")
        self.dateText_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.dateText_5)

        self.timeText_5 = QLabel(self.horizontalLayoutWidget_3)
        self.timeText_5.setObjectName(u"timeText_5")
        self.timeText_5.setFont(font3)
        self.timeText_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.timeText_5)

        self.label_16 = QLabel(self.horizontalLayoutWidget_3)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_16)

        self.systemPageText = QLabel(self.frame_6)
        self.systemPageText.setObjectName(u"systemPageText")
        self.systemPageText.setGeometry(QRect(50, 90, 221, 61))
        self.systemPageText.setFont(font10)
        self.logoImage_5 = QLabel(self.frame_6)
        self.logoImage_5.setObjectName(u"logoImage_5")
        self.logoImage_5.setGeometry(QRect(470, 40, 51, 51))
        self.logoImage_5.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.logoText_5 = QLabel(self.frame_6)
        self.logoText_5.setObjectName(u"logoText_5")
        self.logoText_5.setGeometry(QRect(510, 50, 111, 51))
        self.logoText_5.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.launguageImage = QLabel(self.frame_6)
        self.launguageImage.setObjectName(u"launguageImage")
        self.launguageImage.setGeometry(QRect(60, 200, 111, 91))
        self.launguageImage.setStyleSheet(u"background-color:transparent;\n"
"image: url(:/icon/icon/language.png);")
        self.soundImage = QLabel(self.frame_6)
        self.soundImage.setObjectName(u"soundImage")
        self.soundImage.setGeometry(QRect(60, 320, 121, 91))
        self.soundImage.setStyleSheet(u"background-color:transparent;\n"
"image: url(:/icon/icon/sound.png);")
        self.soundSlider = QSlider(self.frame_6)
        self.soundSlider.setObjectName(u"soundSlider")
        self.soundSlider.setGeometry(QRect(210, 350, 291, 31))
        self.soundSlider.setStyleSheet(u"QSlider::handle:horizontal {\n"
"\n"
"    background-color:rgb(174, 222, 211);\n"
"    width: 18px;\n"
"    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"    border-radius: 3px;\n"
"}")
        self.soundSlider.setValue(0)
        self.soundSlider.setOrientation(Qt.Orientation.Horizontal)
        self.soundValue = QLabel(self.frame_6)
        self.soundValue.setObjectName(u"soundValue")
        self.soundValue.setGeometry(QRect(490, 340, 81, 41))
        self.soundValue.setFont(font)
        self.soundValue.setStyleSheet(u"background-color:transparent;")
        self.soundValue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.comboBox = QComboBox(self.frame_6)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(200, 230, 341, 27))
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        font11 = QFont()
        font11.setPointSize(13)
        font11.setBold(True)
        self.comboBox.setFont(font11)
        self.comboBox.setStyleSheet(u"QComboBox {\n"
"	border-top: 2px solid;\n"
"	border-radius:10px;\n"
"	color:rgb(121, 121, 121);\n"
"	background-color:rgb(229, 229, 229);\n"
"	border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, 		y2:1, stop:0 rgb(183, 183, 183), stop:1 rgb(203, 203, 203));\n"
"}\n"
"\n"
"QComboBox:on { \n"
"	border-top: 2px solid;\n"
"	border-radius:10px;\n"
"	background-color:rgb(229, 229, 229);\n"
"	border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, 		y2:1, stop:0 rgb(183, 183, 183), stop:1 rgb(203, 203, 203));\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 12px;\n"
"	\n"
"	image: url(:/icon/icon/arrow.png);\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-top-right-radius: 10px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 10px;\n"
"	margin-right:2px;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"	color:rgb(121, 121, 121);\n"
"    background: white;\n"
"	border:1px;\n"
"	border-radius:10px;\n"
"}")
        self.comboBox.setEditable(False)
        self.comboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.comboBox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.comboBox.setIconSize(QSize(16, 16))
        self.comboBox.setDuplicatesEnabled(False)
        self.comboBox.setFrame(True)
        self.cancelButton_5 = QPushButton(self.frame_6)
        self.cancelButton_5.setObjectName(u"cancelButton_5")
        self.cancelButton_5.setGeometry(QRect(470, 500, 61, 31))
        self.cancelButton_5.setFont(font4)
        self.cancelButton_5.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.yesButton_5 = QPushButton(self.frame_6)
        self.yesButton_5.setObjectName(u"yesButton_5")
        self.yesButton_5.setGeometry(QRect(540, 500, 61, 31))
        self.yesButton_5.setFont(font4)
        self.yesButton_5.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.stackedWidget.addWidget(self.SystemPage)
        self.InfoPage = QWidget()
        self.InfoPage.setObjectName(u"InfoPage")
        self.frame_8 = QFrame(self.InfoPage)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setGeometry(QRect(0, 0, 651, 541))
        font12 = QFont()
        font12.setBold(False)
        self.frame_8.setFont(font12)
        self.frame_8.setStyleSheet(u"background-color : transparent;\n"
"")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_11 = QFrame(self.frame_8)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setGeometry(QRect(0, 0, 651, 31))
        self.frame_11.setStyleSheet(u"background-color:rgb(174, 222, 211);\n"
"border:0px;")
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_11.setLineWidth(0)
        self.horizontalLayoutWidget_4 = QWidget(self.frame_11)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(0, 0, 661, 31))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setSpacing(100)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.dateText_6 = QLabel(self.horizontalLayoutWidget_4)
        self.dateText_6.setObjectName(u"dateText_6")
        self.dateText_6.setFont(font3)
        self.dateText_6.setStyleSheet(u"margin-left:10px;")
        self.dateText_6.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.dateText_6)

        self.timeText_6 = QLabel(self.horizontalLayoutWidget_4)
        self.timeText_6.setObjectName(u"timeText_6")
        self.timeText_6.setFont(font3)
        self.timeText_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.timeText_6)

        self.label_44 = QLabel(self.horizontalLayoutWidget_4)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_44)

        self.infoPageText = QLabel(self.frame_8)
        self.infoPageText.setObjectName(u"infoPageText")
        self.infoPageText.setGeometry(QRect(50, 90, 221, 61))
        self.infoPageText.setFont(font10)
        self.logoImage_6 = QLabel(self.frame_8)
        self.logoImage_6.setObjectName(u"logoImage_6")
        self.logoImage_6.setGeometry(QRect(470, 40, 51, 51))
        self.logoImage_6.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.logoText_6 = QLabel(self.frame_8)
        self.logoText_6.setObjectName(u"logoText_6")
        self.logoText_6.setGeometry(QRect(510, 50, 111, 51))
        self.logoText_6.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.frame_20 = QFrame(self.frame_8)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setGeometry(QRect(50, 180, 501, 281))
        self.frame_20.setStyleSheet(u"border-radius:15px;\n"
"background-color:rgb(194, 226, 219);")
        self.frame_20.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_20.setLineWidth(0)
        self.horizontalLayoutWidget_5 = QWidget(self.frame_20)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(20, 30, 459, 211))
        self.verticalLayout_3 = QVBoxLayout(self.horizontalLayoutWidget_5)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.nameText = QLabel(self.horizontalLayoutWidget_5)
        self.nameText.setObjectName(u"nameText")
        font13 = QFont()
        font13.setPointSize(20)
        font13.setBold(True)
        self.nameText.setFont(font13)
        self.nameText.setStyleSheet(u"margin-left:1px;")

        self.horizontalLayout_10.addWidget(self.nameText)

        self.nameValue = QLabel(self.horizontalLayoutWidget_5)
        self.nameValue.setObjectName(u"nameValue")
        self.nameValue.setFont(font13)

        self.horizontalLayout_10.addWidget(self.nameValue)

        self.label_65 = QLabel(self.horizontalLayoutWidget_5)
        self.label_65.setObjectName(u"label_65")

        self.horizontalLayout_10.addWidget(self.label_65)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.genderText = QLabel(self.horizontalLayoutWidget_5)
        self.genderText.setObjectName(u"genderText")
        self.genderText.setFont(font13)
        self.genderText.setStyleSheet(u"margin-left:1px;")

        self.horizontalLayout_8.addWidget(self.genderText)

        self.genderValue = QLabel(self.horizontalLayoutWidget_5)
        self.genderValue.setObjectName(u"genderValue")
        self.genderValue.setFont(font13)

        self.horizontalLayout_8.addWidget(self.genderValue)

        self.label_59 = QLabel(self.horizontalLayoutWidget_5)
        self.label_59.setObjectName(u"label_59")

        self.horizontalLayout_8.addWidget(self.label_59)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.typeText = QLabel(self.horizontalLayoutWidget_5)
        self.typeText.setObjectName(u"typeText")
        self.typeText.setFont(font13)
        self.typeText.setStyleSheet(u"margin-left:1px;")

        self.horizontalLayout_9.addWidget(self.typeText)

        self.typeValue = QLabel(self.horizontalLayoutWidget_5)
        self.typeValue.setObjectName(u"typeValue")
        self.typeValue.setFont(font13)

        self.horizontalLayout_9.addWidget(self.typeValue)

        self.label_62 = QLabel(self.horizontalLayoutWidget_5)
        self.label_62.setObjectName(u"label_62")

        self.horizontalLayout_9.addWidget(self.label_62)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.cancelButton_6 = QPushButton(self.frame_8)
        self.cancelButton_6.setObjectName(u"cancelButton_6")
        self.cancelButton_6.setGeometry(QRect(540, 500, 61, 31))
        self.cancelButton_6.setFont(font4)
        self.cancelButton_6.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.frame_20.raise_()
        self.frame_11.raise_()
        self.infoPageText.raise_()
        self.logoImage_6.raise_()
        self.logoText_6.raise_()
        self.cancelButton_6.raise_()
        self.stackedWidget.addWidget(self.InfoPage)
        self.DiaryPage = QWidget()
        self.DiaryPage.setObjectName(u"DiaryPage")
        self.frame_14 = QFrame(self.DiaryPage)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setGeometry(QRect(0, 0, 651, 541))
        self.frame_14.setStyleSheet(u"background-color : transparent;\n"
"")
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_15 = QFrame(self.frame_14)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setGeometry(QRect(0, 0, 651, 31))
        self.frame_15.setStyleSheet(u"background-color:rgb(174, 222, 211);\n"
"border:0px;")
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_15.setLineWidth(0)
        self.horizontalLayoutWidget_9 = QWidget(self.frame_15)
        self.horizontalLayoutWidget_9.setObjectName(u"horizontalLayoutWidget_9")
        self.horizontalLayoutWidget_9.setGeometry(QRect(0, 0, 661, 31))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_5.setSpacing(100)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.dateText_7 = QLabel(self.horizontalLayoutWidget_9)
        self.dateText_7.setObjectName(u"dateText_7")
        self.dateText_7.setFont(font3)
        self.dateText_7.setStyleSheet(u"margin-left:10px;")
        self.dateText_7.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.dateText_7)

        self.timeText_7 = QLabel(self.horizontalLayoutWidget_9)
        self.timeText_7.setObjectName(u"timeText_7")
        self.timeText_7.setFont(font3)
        self.timeText_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.timeText_7)

        self.label_50 = QLabel(self.horizontalLayoutWidget_9)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_50)

        self.diaryText_7 = QLabel(self.frame_14)
        self.diaryText_7.setObjectName(u"diaryText_7")
        self.diaryText_7.setGeometry(QRect(50, 90, 261, 61))
        self.diaryText_7.setFont(font10)
        self.logoImage_7 = QLabel(self.frame_14)
        self.logoImage_7.setObjectName(u"logoImage_7")
        self.logoImage_7.setGeometry(QRect(470, 40, 51, 51))
        self.logoImage_7.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.logoText_7 = QLabel(self.frame_14)
        self.logoText_7.setObjectName(u"logoText_7")
        self.logoText_7.setGeometry(QRect(510, 50, 111, 51))
        self.logoText_7.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.diaryText_7_1 = QLabel(self.frame_14)
        self.diaryText_7_1.setObjectName(u"diaryText_7_1")
        self.diaryText_7_1.setGeometry(QRect(140, 260, 341, 61))
        self.diaryText_7_1.setFont(font6)
        self.diaryText_7_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.diaryButton_7 = QPushButton(self.frame_14)
        self.diaryButton_7.setObjectName(u"diaryButton_7")
        self.diaryButton_7.setGeometry(QRect(200, 340, 231, 41))
        self.diaryButton_7.setFont(font4)
        self.diaryButton_7.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.cancelButton_7 = QPushButton(self.frame_14)
        self.cancelButton_7.setObjectName(u"cancelButton_7")
        self.cancelButton_7.setGeometry(QRect(540, 500, 61, 31))
        self.cancelButton_7.setFont(font4)
        self.cancelButton_7.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.stackedWidget.addWidget(self.DiaryPage)
        self.DiaryIngPage = QWidget()
        self.DiaryIngPage.setObjectName(u"DiaryIngPage")
        self.frame_16 = QFrame(self.DiaryIngPage)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setGeometry(QRect(0, 0, 651, 541))
        self.frame_16.setStyleSheet(u"background-color : transparent;\n"
"")
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_17 = QFrame(self.frame_16)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setGeometry(QRect(0, 0, 651, 31))
        self.frame_17.setStyleSheet(u"background-color:rgb(174, 222, 211);\n"
"border:0px;")
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_17.setLineWidth(0)
        self.horizontalLayoutWidget_10 = QWidget(self.frame_17)
        self.horizontalLayoutWidget_10.setObjectName(u"horizontalLayoutWidget_10")
        self.horizontalLayoutWidget_10.setGeometry(QRect(0, 0, 661, 31))
        self.horizontalLayout_11 = QHBoxLayout(self.horizontalLayoutWidget_10)
        self.horizontalLayout_11.setSpacing(100)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.dateText_8 = QLabel(self.horizontalLayoutWidget_10)
        self.dateText_8.setObjectName(u"dateText_8")
        self.dateText_8.setFont(font3)
        self.dateText_8.setStyleSheet(u"margin-left:10px;")
        self.dateText_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.dateText_8)

        self.timeText_8 = QLabel(self.horizontalLayoutWidget_10)
        self.timeText_8.setObjectName(u"timeText_8")
        self.timeText_8.setFont(font3)
        self.timeText_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_11.addWidget(self.timeText_8)

        self.label_72 = QLabel(self.horizontalLayoutWidget_10)
        self.label_72.setObjectName(u"label_72")
        self.label_72.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_72)

        self.diaryText_8 = QLabel(self.frame_16)
        self.diaryText_8.setObjectName(u"diaryText_8")
        self.diaryText_8.setGeometry(QRect(50, 90, 261, 61))
        self.diaryText_8.setFont(font10)
        self.logoImage_8 = QLabel(self.frame_16)
        self.logoImage_8.setObjectName(u"logoImage_8")
        self.logoImage_8.setGeometry(QRect(470, 40, 51, 51))
        self.logoImage_8.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.logoText_8 = QLabel(self.frame_16)
        self.logoText_8.setObjectName(u"logoText_8")
        self.logoText_8.setGeometry(QRect(510, 50, 111, 51))
        self.logoText_8.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.diaryText_8_1 = QLabel(self.frame_16)
        self.diaryText_8_1.setObjectName(u"diaryText_8_1")
        self.diaryText_8_1.setGeometry(QRect(140, 260, 341, 61))
        self.diaryText_8_1.setFont(font6)
        self.diaryText_8_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.diaryButton_8 = QPushButton(self.frame_16)
        self.diaryButton_8.setObjectName(u"diaryButton_8")
        self.diaryButton_8.setGeometry(QRect(200, 340, 231, 41))
        self.diaryButton_8.setFont(font4)
        self.diaryButton_8.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.stackedWidget.addWidget(self.DiaryIngPage)
        self.DiaryCompletePage = QWidget()
        self.DiaryCompletePage.setObjectName(u"DiaryCompletePage")
        self.frame_18 = QFrame(self.DiaryCompletePage)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setGeometry(QRect(0, 0, 651, 541))
        self.frame_18.setStyleSheet(u"background-color : transparent;\n"
"")
        self.frame_18.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_19 = QFrame(self.frame_18)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setGeometry(QRect(0, 0, 651, 31))
        self.frame_19.setStyleSheet(u"background-color:rgb(174, 222, 211);\n"
"border:0px;")
        self.frame_19.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_19.setLineWidth(0)
        self.horizontalLayoutWidget_11 = QWidget(self.frame_19)
        self.horizontalLayoutWidget_11.setObjectName(u"horizontalLayoutWidget_11")
        self.horizontalLayoutWidget_11.setGeometry(QRect(0, 0, 661, 31))
        self.horizontalLayout_12 = QHBoxLayout(self.horizontalLayoutWidget_11)
        self.horizontalLayout_12.setSpacing(100)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.dateText_9 = QLabel(self.horizontalLayoutWidget_11)
        self.dateText_9.setObjectName(u"dateText_9")
        self.dateText_9.setFont(font3)
        self.dateText_9.setStyleSheet(u"margin-left:10px;")
        self.dateText_9.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.dateText_9)

        self.timeText_9 = QLabel(self.horizontalLayoutWidget_11)
        self.timeText_9.setObjectName(u"timeText_9")
        self.timeText_9.setFont(font3)
        self.timeText_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_12.addWidget(self.timeText_9)

        self.label_79 = QLabel(self.horizontalLayoutWidget_11)
        self.label_79.setObjectName(u"label_79")
        self.label_79.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_79)

        self.diaryText_9 = QLabel(self.frame_18)
        self.diaryText_9.setObjectName(u"diaryText_9")
        self.diaryText_9.setGeometry(QRect(50, 90, 261, 61))
        self.diaryText_9.setFont(font10)
        self.logoImage_9 = QLabel(self.frame_18)
        self.logoImage_9.setObjectName(u"logoImage_9")
        self.logoImage_9.setGeometry(QRect(470, 40, 51, 51))
        self.logoImage_9.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0.png);")
        self.logoText_9 = QLabel(self.frame_18)
        self.logoText_9.setObjectName(u"logoText_9")
        self.logoText_9.setGeometry(QRect(510, 50, 111, 51))
        self.logoText_9.setStyleSheet(u"image: url(:/icon/icon/\ub85c\uace0_\uae00.png);\n"
"background-color : transparent;")
        self.diaryText_9_1 = QLabel(self.frame_18)
        self.diaryText_9_1.setObjectName(u"diaryText_9_1")
        self.diaryText_9_1.setGeometry(QRect(140, 260, 371, 61))
        self.diaryText_9_1.setFont(font6)
        self.diaryText_9_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.diaryButton_9 = QPushButton(self.frame_18)
        self.diaryButton_9.setObjectName(u"diaryButton_9")
        self.diaryButton_9.setGeometry(QRect(200, 340, 231, 41))
        self.diaryButton_9.setFont(font4)
        self.diaryButton_9.setStyleSheet(u"border-radius:10px;\n"
"background-color:rgb(174, 222, 211);\n"
"border-bottom:2px solid;\n"
"border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(163, 163, 163), stop:1 rgb(203, 203, 203));")
        self.stackedWidget.addWidget(self.DiaryCompletePage)

        self.verticalLayout_2.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 663, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.BackButton.clicked.connect(MainWindow.goToWifiPage)
        self.nextButton_2.clicked.connect(MainWindow.goToMainPage)
        self.soundSlider.valueChanged.connect(self.soundValue.setNum)
        self.settingButton.clicked.connect(MainWindow.goToSettingPage)
        self.cancelButton_4.clicked.connect(MainWindow.goToMainPage)
        self.cancelButton_6.clicked.connect(MainWindow.goToSettingPage)
        self.cancelButton_7.clicked.connect(MainWindow.goToMainPage)
        self.diaryButton_9.clicked.connect(MainWindow.goToDiaryPage)
        self.infoButton.clicked.connect(MainWindow.goToInfoPage)
        self.systemButton.clicked.connect(MainWindow.goToSystemPage)
        self.yesButton_5.clicked.connect(MainWindow.goToSettingPage)
        self.cancelButton_5.clicked.connect(MainWindow.goToSettingPage)
        self.diaryButton_7.clicked.connect(MainWindow.goToDiaryIngPage)
        self.diaryButton_8.clicked.connect(MainWindow.goToCompletePage)
        self.yesButton_1.clicked.connect(MainWindow.goToQRPage)
        self.WIFIButton.clicked.connect(MainWindow.goToWifiSelectPage)
        self.diaryButton_9.clicked.connect(MainWindow.goToMainPage)
        self.diaryButton_3.clicked.connect(MainWindow.goToDiaryPage)
        self.infoImage.clicked.connect(MainWindow.goToInfoPage)
        self.infoText.clicked.connect(MainWindow.goToInfoPage)
        self.systemImage.clicked.connect(MainWindow.goToSystemPage)
        self.systemText.clicked.connect(MainWindow.goToSystemPage)
        self.diaryImage.clicked.connect(MainWindow.goToDiaryPage)
        self.diaryText.clicked.connect(MainWindow.goToDiaryPage)
        self.settingImage.clicked.connect(MainWindow.goToSettingPage)
        self.settingText.clicked.connect(MainWindow.goToSettingPage)
        self.logoImage_2.clicked.connect(MainWindow.goToWifiSelectPage)
        self.logoImage_3.clicked.connect(MainWindow.goToQRPage)
        self.pwdImage.clicked.connect(MainWindow.TextToggle)

        self.stackedWidget.setCurrentIndex(2)
        self.comboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.networkText1.setText(QCoreApplication.translate("MainWindow", u"\ub124\ud2b8\uc6cc\ud06c", None))
        self.reloadImage.setText("")
        self.WIFIButton.setText(QCoreApplication.translate("MainWindow", u"SSAFY801", None))
        self.WIFIButton1.setText(QCoreApplication.translate("MainWindow", u"SSAFY801", None))
        self.networkText.setText(QCoreApplication.translate("MainWindow", u"\ub124\ud2b8\uc6cc\ud06c \uc124\uc815", None))
        self.logoText_0.setText("")
        self.logoImage_0.setText("")
        self.pwdPlacehold.setText(QCoreApplication.translate("MainWindow", u"\uc774 \ubd80\ubd84\uc744 \ud074\ub9ad\ud558\uace0 \ube44\ubc00\ubc88\ud638\ub97c \uc785\ub825\ud558\uc138\uc694", None))
        self.pwdImage.setText("")
        self.networkName.setText(QCoreApplication.translate("MainWindow", u"SSAFY801", None))
        self.BackButton.setText("")
        self.pwdText.setText(QCoreApplication.translate("MainWindow", u"\ube44\ubc00\ubc88\ud638", None))
        self.yesButton_1.setText(QCoreApplication.translate("MainWindow", u"\ud655\uc778", None))
        self.logoImage_1.setText("")
        self.logoText_1.setText("")
        self.nextButton_2.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc74c", None))
        self.QRText2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">\ud68c\uc6d0\uac00\uc785\uc774 \uc644\ub8cc\ub418\uba74 \uc790\ub3d9\uc73c\ub85c \ud654\uba74\uc774 \ubc14\ub01d\ub2c8\ub2e4.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">\ud654\uba74\uc774 \ubc14\ub00c\uc9c0 \uc54a\uc744 \uacbd\uc6b0"
                        " [\ub2e4\uc74c] \ubc84\ud2bc\uc744 \ub20c\ub7ec\uc8fc\uc138\uc694.</span></p></body></html>", None))
        self.QRText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt; font-weight:700;\">QR\uc744 \uc778\uc2dd\ud558\uc5ec</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt; font-weight:700;\">\ud68c\uc6d0\uac00\uc785\uc744 \ud574\uc8fc\uc138\uc694!</span></p></body></html>", None))
        self.characterImage.setText("")
        self.logoImage_2.setText("")
        self.logoText_2.setText("")
        self.QRText3.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:700; color:#ff0000;\">\uc544\uc9c1 \ud68c\uc6d0\uac00\uc785\uc774</span></p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:700; color:#ff0000;\">\uc644\ub8cc\ub418\uc9c0 \uc54a\uc558\uc2b5\ub2c8"
                        "\ub2e4</span></p></body></html>", None))
        self.dateText_3.setText(QCoreApplication.translate("MainWindow", u"2024-07-25", None))
        self.timeText_3.setText(QCoreApplication.translate("MainWindow", u"\uc624\uc804 9:00", None))
        self.label_5.setText("")
        self.settingText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:33pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\">\uc124\uc815</span></p></body></html>", None))
        self.greetings.setText(QCoreApplication.translate("MainWindow", u"\uc548\ub155\ud558\uc138\uc694 \uc9f1\uc6a9\uc774 \uac00\ubc29\uc774\uc5d0\uc694", None))
        self.weatherImage.setText("")
        self.logoImage_3.setText("")
        self.weatherText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\">H : 29\u2103</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\">L : 23\u2103</span></p></body></html>", None))
        self.weatherButton.setText("")
        self.diaryButton_3.setText("")
        self.settingButton.setText("")
        self.logoText_3.setText("")
        self.diaryImage.setText("")
        self.diaryText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'\ub9d1\uc740 \uace0\ub515'; font-size:33pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">\ub2e4\uc774\uc5b4\ub9ac</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">\uc791\uc131</span></p></body></html>", None))
        self.settingImage.setText("")
        self.dateText_4.setText(QCoreApplication.translate("MainWindow", u"2024-07-25", None))
        self.timeText_4.setText(QCoreApplication.translate("MainWindow", u"\uc624\uc804 9:00", None))
        self.label_13.setText("")
        self.settingPageText.setText(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
        self.logoImage_4.setText("")
        self.infoButton.setText("")
        self.systemButton.setText("")
        self.logoText_4.setText("")
        self.systemImage.setText("")
        self.infoImage.setText("")
        self.infoText.setText(QCoreApplication.translate("MainWindow", u"\uc5d0\ubc84\ud3ab", None))
        self.systemText.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc2a4\ud15c", None))
        self.cancelButton_4.setText(QCoreApplication.translate("MainWindow", u"\ucde8\uc18c", None))
        self.dateText_5.setText(QCoreApplication.translate("MainWindow", u"2024-07-25", None))
        self.timeText_5.setText(QCoreApplication.translate("MainWindow", u"\uc624\uc804 9:00", None))
        self.label_16.setText("")
        self.systemPageText.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc2a4\ud15c \uc124\uc815", None))
        self.logoImage_5.setText("")
        self.logoText_5.setText("")
        self.launguageImage.setText("")
        self.soundImage.setText("")
        self.soundValue.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\ud55c\uad6d\uc5b4", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\uc601\uc5b4", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\uc77c\ubcf8\uc5b4", None))

        self.cancelButton_5.setText(QCoreApplication.translate("MainWindow", u"\ucde8\uc18c", None))
        self.yesButton_5.setText(QCoreApplication.translate("MainWindow", u"\ud655\uc778", None))
        self.dateText_6.setText(QCoreApplication.translate("MainWindow", u"2024-07-25", None))
        self.timeText_6.setText(QCoreApplication.translate("MainWindow", u"\uc624\uc804 9:00", None))
        self.label_44.setText("")
        self.infoPageText.setText(QCoreApplication.translate("MainWindow", u"\uc5d0\ubc84\ud3ab \uc815\ubcf4", None))
        self.logoImage_6.setText("")
        self.logoText_6.setText("")
        self.nameText.setText(QCoreApplication.translate("MainWindow", u"\uc774\ub984", None))
        self.nameValue.setText(QCoreApplication.translate("MainWindow", u"\uc9f1\uc6a9\uc774", None))
        self.label_65.setText("")
        self.genderText.setText(QCoreApplication.translate("MainWindow", u"\uc131\ubcc4", None))
        self.genderValue.setText(QCoreApplication.translate("MainWindow", u"\ub0a8", None))
        self.label_59.setText("")
        self.typeText.setText(QCoreApplication.translate("MainWindow", u"\uc131\uaca9", None))
        self.typeValue.setText(QCoreApplication.translate("MainWindow", u"\ud65c\ubc1c", None))
        self.label_62.setText("")
        self.cancelButton_6.setText(QCoreApplication.translate("MainWindow", u"\ucde8\uc18c", None))
        self.dateText_7.setText(QCoreApplication.translate("MainWindow", u"2024-07-25", None))
        self.timeText_7.setText(QCoreApplication.translate("MainWindow", u"\uc624\uc804 9:00", None))
        self.label_50.setText("")
        self.diaryText_7.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131", None))
        self.logoImage_7.setText("")
        self.logoText_7.setText("")
        self.diaryText_7_1.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac\ub97c \uc791\uc131 \ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", None))
        self.diaryButton_7.setText(QCoreApplication.translate("MainWindow", u"\uc791\uc131 \uc2dc\uc791", None))
        self.cancelButton_7.setText(QCoreApplication.translate("MainWindow", u"\ucde8\uc18c", None))
        self.dateText_8.setText(QCoreApplication.translate("MainWindow", u"2024-07-25", None))
        self.timeText_8.setText(QCoreApplication.translate("MainWindow", u"\uc624\uc804 9:00", None))
        self.label_72.setText("")
        self.diaryText_8.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131", None))
        self.logoImage_8.setText("")
        self.logoText_8.setText("")
        self.diaryText_8_1.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131 \uc911....", None))
        self.diaryButton_8.setText(QCoreApplication.translate("MainWindow", u"\uc791\uc131 \uc885\ub8cc", None))
        self.dateText_9.setText(QCoreApplication.translate("MainWindow", u"2024-07-25", None))
        self.timeText_9.setText(QCoreApplication.translate("MainWindow", u"\uc624\uc804 9:00", None))
        self.label_79.setText("")
        self.diaryText_9.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131", None))
        self.logoImage_9.setText("")
        self.logoText_9.setText("")
        self.diaryText_9_1.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc774\uc5b4\ub9ac \uc791\uc131\uc774 \uc644\ub8cc\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", None))
        self.diaryButton_9.setText(QCoreApplication.translate("MainWindow", u"\ud648", None))
    # retranslateUi




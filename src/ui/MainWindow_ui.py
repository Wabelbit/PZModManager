# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_Save = QAction(MainWindow)
        self.action_Save.setObjectName(u"action_Save")
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        self.action_Quit.setMenuRole(QAction.QuitRole)
        self.action_SaveAll = QAction(MainWindow)
        self.action_SaveAll.setObjectName(u"action_SaveAll")
        self.action_ShowDetails = QAction(MainWindow)
        self.action_ShowDetails.setObjectName(u"action_ShowDetails")
        self.action_ShowDetails.setCheckable(True)
        self.action_SelectAll = QAction(MainWindow)
        self.action_SelectAll.setObjectName(u"action_SelectAll")
        self.action_About = QAction(MainWindow)
        self.action_About.setObjectName(u"action_About")
        self.action_About.setMenuRole(QAction.AboutRole)
        self.action_AboutQt = QAction(MainWindow)
        self.action_AboutQt.setObjectName(u"action_AboutQt")
        self.action_AboutQt.setMenuRole(QAction.AboutQtRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addAction(self.action_SaveAll)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Quit)
        self.menuView.addAction(self.action_ShowDetails)
        self.menuEdit.addAction(self.action_SelectAll)
        self.menuHelp.addAction(self.action_About)
        self.menuHelp.addAction(self.action_AboutQt)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PZ Mod Manager", None))
        self.action_Save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.action_Save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.action_Quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_SaveAll.setText(QCoreApplication.translate("MainWindow", u"Save All", None))
#if QT_CONFIG(shortcut)
        self.action_SaveAll.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_ShowDetails.setText(QCoreApplication.translate("MainWindow", u"Show details", None))
#if QT_CONFIG(shortcut)
        self.action_ShowDetails.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.action_SelectAll.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
#if QT_CONFIG(shortcut)
        self.action_SelectAll.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.action_About.setText(QCoreApplication.translate("MainWindow", u"About PZ Mod Manager", None))
        self.action_AboutQt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi


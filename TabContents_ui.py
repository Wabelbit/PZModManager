# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabContents.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_TabContents(object):
    def setupUi(self, TabContents):
        if not TabContents.objectName():
            TabContents.setObjectName(u"TabContents")
        TabContents.resize(789, 664)
        self.horizontalLayout = QHBoxLayout(TabContents)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.list_disabled_2 = QListWidget(TabContents)
        QListWidgetItem(self.list_disabled_2)
        QListWidgetItem(self.list_disabled_2)
        self.list_disabled_2.setObjectName(u"list_disabled_2")
        self.list_disabled_2.setDragDropMode(QAbstractItemView.DragOnly)
        self.list_disabled_2.setDefaultDropAction(Qt.IgnoreAction)
        self.list_disabled_2.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_disabled_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_disabled_2.setIconSize(QSize(16, 16))
        self.list_disabled_2.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_disabled_2.setMovement(QListView.Free)

        self.horizontalLayout.addWidget(self.list_disabled_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.button_enable = QPushButton(TabContents)
        self.button_enable.setObjectName(u"button_enable")

        self.verticalLayout_2.addWidget(self.button_enable)

        self.button_disable = QPushButton(TabContents)
        self.button_disable.setObjectName(u"button_disable")

        self.verticalLayout_2.addWidget(self.button_disable)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.list_disabled = QListWidget(TabContents)
        QListWidgetItem(self.list_disabled)
        QListWidgetItem(self.list_disabled)
        self.list_disabled.setObjectName(u"list_disabled")
        self.list_disabled.setDragDropMode(QAbstractItemView.DragOnly)
        self.list_disabled.setDefaultDropAction(Qt.IgnoreAction)
        self.list_disabled.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_disabled.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_disabled.setIconSize(QSize(16, 16))
        self.list_disabled.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_disabled.setMovement(QListView.Free)

        self.horizontalLayout.addWidget(self.list_disabled)


        self.retranslateUi(TabContents)

        QMetaObject.connectSlotsByName(TabContents)
    # setupUi

    def retranslateUi(self, TabContents):
        TabContents.setWindowTitle(QCoreApplication.translate("TabContents", u"Form", None))

        __sortingEnabled = self.list_disabled_2.isSortingEnabled()
        self.list_disabled_2.setSortingEnabled(False)
        ___qlistwidgetitem = self.list_disabled_2.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("TabContents", u"Example Item 1", None));
        ___qlistwidgetitem1 = self.list_disabled_2.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("TabContents", u"Example Item 2", None));
        self.list_disabled_2.setSortingEnabled(__sortingEnabled)

#if QT_CONFIG(tooltip)
        self.list_disabled_2.setToolTip(QCoreApplication.translate("TabContents", u"Available mods and workshop items", None))
#endif // QT_CONFIG(tooltip)
        self.button_enable.setText(QCoreApplication.translate("TabContents", u"Enable -->", None))
        self.button_disable.setText(QCoreApplication.translate("TabContents", u"<-- Disable", None))

        __sortingEnabled1 = self.list_disabled.isSortingEnabled()
        self.list_disabled.setSortingEnabled(False)
        ___qlistwidgetitem2 = self.list_disabled.item(0)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("TabContents", u"Example Item 1", None));
        ___qlistwidgetitem3 = self.list_disabled.item(1)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("TabContents", u"Example Item 2", None));
        self.list_disabled.setSortingEnabled(__sortingEnabled1)

#if QT_CONFIG(tooltip)
        self.list_disabled.setToolTip(QCoreApplication.translate("TabContents", u"Available mods and workshop items", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi


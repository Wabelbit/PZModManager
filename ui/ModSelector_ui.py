# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ModSelector.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLabel,
    QListView, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_ModSelector(object):
    def setupUi(self, ModSelector):
        if not ModSelector.objectName():
            ModSelector.setObjectName(u"ModSelector")
        ModSelector.resize(800, 600)
        self.horizontalLayout = QHBoxLayout(ModSelector)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ModSelector)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.list_disabled = QListView(ModSelector)
        self.list_disabled.setObjectName(u"list_disabled")
        self.list_disabled.setDragDropMode(QAbstractItemView.DragOnly)
        self.list_disabled.setDefaultDropAction(Qt.IgnoreAction)
        self.list_disabled.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_disabled.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_disabled.setIconSize(QSize(16, 16))
        self.list_disabled.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_disabled.setMovement(QListView.Free)

        self.verticalLayout.addWidget(self.list_disabled)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.button_enable = QPushButton(ModSelector)
        self.button_enable.setObjectName(u"button_enable")

        self.verticalLayout_2.addWidget(self.button_enable)

        self.button_disable = QPushButton(ModSelector)
        self.button_disable.setObjectName(u"button_disable")

        self.verticalLayout_2.addWidget(self.button_disable)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(ModSelector)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.list_enabled = QListView(ModSelector)
        self.list_enabled.setObjectName(u"list_enabled")
        self.list_enabled.setDragDropMode(QAbstractItemView.DragOnly)
        self.list_enabled.setDefaultDropAction(Qt.IgnoreAction)
        self.list_enabled.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_enabled.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_enabled.setIconSize(QSize(16, 16))
        self.list_enabled.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_enabled.setMovement(QListView.Free)

        self.verticalLayout_3.addWidget(self.list_enabled)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        QWidget.setTabOrder(self.list_disabled, self.button_enable)
        QWidget.setTabOrder(self.button_enable, self.list_enabled)
        QWidget.setTabOrder(self.list_enabled, self.button_disable)

        self.retranslateUi(ModSelector)

        QMetaObject.connectSlotsByName(ModSelector)
    # setupUi

    def retranslateUi(self, ModSelector):
        ModSelector.setWindowTitle(QCoreApplication.translate("ModSelector", u"ModSelector", None))
        self.label.setText(QCoreApplication.translate("ModSelector", u"Available items", None))
#if QT_CONFIG(tooltip)
        self.list_disabled.setToolTip(QCoreApplication.translate("ModSelector", u"Available mods and workshop items", None))
#endif // QT_CONFIG(tooltip)
        self.button_enable.setText(QCoreApplication.translate("ModSelector", u"Enable -->", None))
        self.button_disable.setText(QCoreApplication.translate("ModSelector", u"<-- Disable", None))
        self.label_2.setText(QCoreApplication.translate("ModSelector", u"Enabled items", None))
#if QT_CONFIG(tooltip)
        self.list_enabled.setToolTip(QCoreApplication.translate("ModSelector", u"Available mods and workshop items", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi


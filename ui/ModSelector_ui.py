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
    QLayout, QLineEdit, QListView, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ModSelector(object):
    def setupUi(self, ModSelector):
        if not ModSelector.objectName():
            ModSelector.setObjectName(u"ModSelector")
        ModSelector.resize(800, 600)
        self.verticalLayout_2 = QVBoxLayout(ModSelector)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_disabled = QLabel(ModSelector)
        self.label_disabled.setObjectName(u"label_disabled")

        self.horizontalLayout.addWidget(self.label_disabled)

        self.label_disabledCount = QLabel(ModSelector)
        self.label_disabledCount.setObjectName(u"label_disabledCount")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_disabledCount.sizePolicy().hasHeightForWidth())
        self.label_disabledCount.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_disabledCount)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.lineEdit_filterDisabled = QLineEdit(ModSelector)
        self.lineEdit_filterDisabled.setObjectName(u"lineEdit_filterDisabled")
        self.lineEdit_filterDisabled.setMaxLength(255)
        self.lineEdit_filterDisabled.setClearButtonEnabled(True)

        self.verticalLayout.addWidget(self.lineEdit_filterDisabled)

        self.list_disabledMods = QListView(ModSelector)
        self.list_disabledMods.setObjectName(u"list_disabledMods")
        self.list_disabledMods.setDragDropMode(QAbstractItemView.DragOnly)
        self.list_disabledMods.setDefaultDropAction(Qt.IgnoreAction)
        self.list_disabledMods.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_disabledMods.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_disabledMods.setIconSize(QSize(16, 16))
        self.list_disabledMods.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_disabledMods.setMovement(QListView.Free)

        self.verticalLayout.addWidget(self.list_disabledMods)

        self.button_enable = QPushButton(ModSelector)
        self.button_enable.setObjectName(u"button_enable")

        self.verticalLayout.addWidget(self.button_enable)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_enabled = QLabel(ModSelector)
        self.label_enabled.setObjectName(u"label_enabled")

        self.horizontalLayout_4.addWidget(self.label_enabled)

        self.label_enabledCount = QLabel(ModSelector)
        self.label_enabledCount.setObjectName(u"label_enabledCount")
        sizePolicy.setHeightForWidth(self.label_enabledCount.sizePolicy().hasHeightForWidth())
        self.label_enabledCount.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.label_enabledCount)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.lineEdit_filterEnabled = QLineEdit(ModSelector)
        self.lineEdit_filterEnabled.setObjectName(u"lineEdit_filterEnabled")
        self.lineEdit_filterEnabled.setMaxLength(255)
        self.lineEdit_filterEnabled.setClearButtonEnabled(True)

        self.verticalLayout_3.addWidget(self.lineEdit_filterEnabled)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.list_enabledMods = QListView(ModSelector)
        self.list_enabledMods.setObjectName(u"list_enabledMods")
        self.list_enabledMods.setDragDropMode(QAbstractItemView.DragOnly)
        self.list_enabledMods.setDefaultDropAction(Qt.IgnoreAction)
        self.list_enabledMods.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_enabledMods.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list_enabledMods.setIconSize(QSize(16, 16))
        self.list_enabledMods.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list_enabledMods.setMovement(QListView.Free)

        self.horizontalLayout_2.addWidget(self.list_enabledMods)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetFixedSize)
        self.button_moveUp = QPushButton(ModSelector)
        self.button_moveUp.setObjectName(u"button_moveUp")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_moveUp.sizePolicy().hasHeightForWidth())
        self.button_moveUp.setSizePolicy(sizePolicy1)
        self.button_moveUp.setMaximumSize(QSize(25, 16777215))

        self.verticalLayout_4.addWidget(self.button_moveUp)

        self.button_moveDown = QPushButton(ModSelector)
        self.button_moveDown.setObjectName(u"button_moveDown")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.button_moveDown.sizePolicy().hasHeightForWidth())
        self.button_moveDown.setSizePolicy(sizePolicy2)
        self.button_moveDown.setMaximumSize(QSize(25, 16777215))

        self.verticalLayout_4.addWidget(self.button_moveDown)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.button_disable = QPushButton(ModSelector)
        self.button_disable.setObjectName(u"button_disable")

        self.verticalLayout_3.addWidget(self.button_disable)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.widget_modDetails = QWidget(ModSelector)
        self.widget_modDetails.setObjectName(u"widget_modDetails")

        self.verticalLayout_2.addWidget(self.widget_modDetails)

        QWidget.setTabOrder(self.lineEdit_filterDisabled, self.list_disabledMods)
        QWidget.setTabOrder(self.list_disabledMods, self.button_enable)
        QWidget.setTabOrder(self.button_enable, self.lineEdit_filterEnabled)
        QWidget.setTabOrder(self.lineEdit_filterEnabled, self.list_enabledMods)
        QWidget.setTabOrder(self.list_enabledMods, self.button_disable)
        QWidget.setTabOrder(self.button_disable, self.button_moveUp)
        QWidget.setTabOrder(self.button_moveUp, self.button_moveDown)

        self.retranslateUi(ModSelector)
    # setupUi

    def retranslateUi(self, ModSelector):
        ModSelector.setWindowTitle(QCoreApplication.translate("ModSelector", u"ModSelector", None))
        self.label_disabled.setText(QCoreApplication.translate("ModSelector", u"Available items", None))
        self.label_disabledCount.setText(QCoreApplication.translate("ModSelector", u"(420)", None))
        self.lineEdit_filterDisabled.setPlaceholderText(QCoreApplication.translate("ModSelector", u"Search...", None))
#if QT_CONFIG(tooltip)
        self.list_disabledMods.setToolTip(QCoreApplication.translate("ModSelector", u"Available mods and workshop items", None))
#endif // QT_CONFIG(tooltip)
        self.button_enable.setText(QCoreApplication.translate("ModSelector", u"Enable selected \u2192", None))
        self.label_enabled.setText(QCoreApplication.translate("ModSelector", u"Enabled items", None))
        self.label_enabledCount.setText(QCoreApplication.translate("ModSelector", u"(69)", None))
        self.lineEdit_filterEnabled.setPlaceholderText(QCoreApplication.translate("ModSelector", u"Search...", None))
#if QT_CONFIG(tooltip)
        self.list_enabledMods.setToolTip(QCoreApplication.translate("ModSelector", u"Available mods and workshop items", None))
#endif // QT_CONFIG(tooltip)
        self.button_moveUp.setText(QCoreApplication.translate("ModSelector", u"\u2191", None))
        self.button_moveDown.setText(QCoreApplication.translate("ModSelector", u"\u2193", None))
        self.button_disable.setText(QCoreApplication.translate("ModSelector", u"\u2190 Disable selected", None))
    # retranslateUi


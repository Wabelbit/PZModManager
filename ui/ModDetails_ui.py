# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ModDetails.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ModDetails(object):
    def setupUi(self, ModDetails):
        if not ModDetails.objectName():
            ModDetails.setObjectName(u"ModDetails")
        ModDetails.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(ModDetails)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label = QLabel(ModDetails)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.label_3 = QLabel(ModDetails)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(ModDetails)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_4 = QLabel(ModDetails)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(ModDetails)

        QMetaObject.connectSlotsByName(ModDetails)
    # setupUi

    def retranslateUi(self, ModDetails):
        ModDetails.setWindowTitle(QCoreApplication.translate("ModDetails", u"ModDetails", None))
        self.label.setText(QCoreApplication.translate("ModDetails", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("ModDetails", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("ModDetails", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("ModDetails", u"TextLabel", None))
    # retranslateUi


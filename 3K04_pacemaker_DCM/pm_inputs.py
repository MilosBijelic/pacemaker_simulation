# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(803, 552)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(210, 150, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(210, 200, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(210, 250, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(210, 290, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(410, 290, 221, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_2.setGeometry(QtCore.QRect(410, 246, 221, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_3.setGeometry(QtCore.QRect(410, 150, 221, 31))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_4.setGeometry(QtCore.QRect(410, 200, 221, 31))
        self.textEdit_4.setObjectName("textEdit_4")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(540, 340, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 340, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(714, 530, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(760, 10, 31, 28))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Pacemaker"))
        self.label_2.setText(_translate("Dialog", "Pusle Width:"))
        self.label_3.setText(_translate("Dialog", "Pulse Amplitude:"))
        self.label_4.setText(_translate("Dialog", "Heart Rate:"))
        self.label_5.setText(_translate("Dialog", "Chamber to Pace:"))
        self.pushButton.setText(_translate("Dialog", "Go!"))
        self.pushButton_2.setText(_translate("Dialog", "Update"))
        self.label_6.setText(_translate("Dialog", "Version 0.2"))
        self.pushButton_3.setText(_translate("Dialog", "X"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


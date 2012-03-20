#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2011-9-2

@author: tianwei

func: 文件夹导入文件子程序
'''

from PyQt4 import QtCore, QtGui
#本地选中文件名
fileName = "./filelist.txt"
prefileDialog = []          

class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        browseButton = self.createButton("&Browse...", self.browse)
        findButton = self.createButton("&Find", self.find)
        savedButton = self.createButton("&Saved",self.saved)

        self.fileComboBox = self.createComboBox("*.pcap|*.p|*.cap")
        self.textComboBox = self.createComboBox()
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())

        fileLabel = QtGui.QLabel("Named:")
        textLabel = QtGui.QLabel("Containing text:")
        directoryLabel = QtGui.QLabel("In directory:")
        self.filesFoundLabel = QtGui.QLabel()

        self.createFilesTable()

        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(savedButton)
        buttonsLayout.addWidget(findButton)
        

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(fileLabel, 0, 0)
        mainLayout.addWidget(self.fileComboBox, 0, 1, 1, 2)
        mainLayout.addWidget(textLabel, 1, 0)
        mainLayout.addWidget(self.textComboBox, 1, 1, 1, 2)
        mainLayout.addWidget(directoryLabel, 2, 0)
        mainLayout.addWidget(self.directoryComboBox, 2, 1)
        mainLayout.addWidget(browseButton, 2, 2)
        mainLayout.addWidget(self.filesTable, 3, 0, 1, 3)
        mainLayout.addWidget(self.filesFoundLabel, 4, 0)
        mainLayout.addLayout(buttonsLayout, 5, 0, 1, 3)
        self.setLayout(mainLayout)

        self.setWindowTitle("Find Files")
        self.resize(700, 700)

    def saved(self):
        #保存列表
        selectedList = self.filesTable.selectedItems()
        i = 0
        file =open(fileName,"w")
        while i < len(selectedList):
            item = (selectedList[i])
            tmp = self.currentDir.absoluteFilePath(item.text())
            prefileDialog.append(tmp)
            tmp = tmp + '\n'
            file.write(str(tmp))
            i = i + 2
        file.close()
        sys.exit(1)
    
    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Find Files",
                QtCore.QDir.currentPath())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(self.directoryComboBox.findText(directory))

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def find(self):
        self.filesTable.setRowCount(0)

        fileName = self.fileComboBox.currentText()
        text = self.textComboBox.currentText()
        path = self.directoryComboBox.currentText()

        self.updateComboBox(self.fileComboBox)
        self.updateComboBox(self.textComboBox)
        self.updateComboBox(self.directoryComboBox)

        self.currentDir = QtCore.QDir(path)

        nameList = fileName.split('|')
        for sigName in  nameList:
            if not sigName:
                sigName = "*"
            files = self.currentDir.entryList([sigName],
                    QtCore.QDir.Files | QtCore.QDir.NoSymLinks) 
            
            if text:
                files = self.findFiles(files, text)
            self.showFiles(files)

    def findFiles(self, files, text):
        progressDialog = QtGui.QProgressDialog(self)

        progressDialog.setCancelButtonText("&Cancel")
        progressDialog.setRange(0, files.count())
        progressDialog.setWindowTitle("Find Files")

        foundFiles = []

        for i in range(files.count()):
            progressDialog.setValue(i)
            progressDialog.setLabelText("Searching file number %d of %d..." % (i, files.count()))
            QtGui.qApp.processEvents()

            if progressDialog.wasCanceled():
                break

            inFile = QtCore.QFile(self.currentDir.absoluteFilePath(files[i]))

            if inFile.open(QtCore.QIODevice.ReadOnly):
                stream = QtCore.QTextStream(inFile)
                while not stream.atEnd():
                    if progressDialog.wasCanceled():
                        break
                    line = stream.readLine()
                    if text in line:
                        foundFiles.append(files[i])
                        break

        progressDialog.close()

        return foundFiles

    def showFiles(self, files):
        for fn in files:
            file = QtCore.QFile(self.currentDir.absoluteFilePath(fn))
            size = QtCore.QFileInfo(file).size()

            fileNameItem = QtGui.QTableWidgetItem(fn)
            fileNameItem.setFlags(fileNameItem.flags() ^ QtCore.Qt.ItemIsEditable)
            sizeItem = QtGui.QTableWidgetItem("%d KB" % (int((size + 1023) / 1024)))
            sizeItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ QtCore.Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

        self.filesFoundLabel.setText("%d file(s) found (Double click on a file to open it)" % len(files))

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Preferred)
        return comboBox

    def createFilesTable(self):
        self.filesTable = QtGui.QTableWidget(0, 2)
        self.filesTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size"))
        self.filesTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)

        self.filesTable.cellActivated.connect(self.openFileOfItem)

    def openFileOfItem(self, row, column):
        item = self.filesTable.item(row, 0)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.currentDir.absoluteFilePath(item.text())))

def printList():
    for tmp in prefileDialog:
        print tmp
        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    #print printList()
    sys.exit(app.exec_())

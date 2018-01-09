from PySide import QtCore, QtGui



class DynamicGridlayout(QtGui.QWidget):
    def __init__(self):
        super(DynamicGridlayout,self).__init__()
        mainLayout = QtGui.QVBoxLayout(self)

        grid = QtGui.QGridLayout()
        # you can directly control the spacing here
        grid.setSpacing(20)

        for row in xrange(5):
            grid.addWidget(QtGui.QLabel("Text"), row, 0,
                           1, 1, QtCore.Qt.AlignTop)
            grid.addWidget(QtGui.QLabel(str(row)), row, 1,
                           1, 1, QtCore.Qt.AlignTop)
            grid.addWidget(QtGui.QPushButton('TESt'), row, 2,
                           1, 1, QtCore.Qt.AlignTop)

        mainLayout.addLayout(grid)
        mainLayout.addStretch()
        self.setLayout(mainLayout)





if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = DynamicGridlayout()
    dialog.show()
    sys.exit(app.exec_())
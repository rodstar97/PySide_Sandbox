import sys
from PyQt4 import QtGui, QtCore




class Button(QtGui.QPushButton):
    def __init__(self,name="", height=0, width=0, parent=None,*args):
        super(Button, self).__init__()
        self.setText(name)
        if height:
            self.setFixedHeight(height)
        if width:
            self.setFixedWidth(width)
        else:
            self.setFixedHeight(55)
            self.setFixedWidth(55)

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        mimeData = QtCore.QMimeData()
        #mimeData.setText('%d,%d' % (e.x(), e.y()))
        mimeData.setText(self.text())

        pixmap = QtGui.QPixmap.grabWidget(self)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(e.pos())

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'

    def mousePressEvent(self, e):
        QtGui.QPushButton.mousePressEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            print 'press'




class Shelf(QtGui.QWidget):
    def __init__(self):
        super(Shelf, self).__init__()
        self.layout = FlowLayout()
        for i in range(4):
            self.layout.addWidget(Button("button_{}".format(i), height = int(i*10) ,width = (i*10) ))
        self.setLayout(self.layout)




class Test(QtGui.QWidget):
    def __init__(self):
        super(Test,self).__init__()
        self.layout = QtGui.QVBoxLayout()
        self.tablayout = QtGui.QTabWidget()
        for i in range(5):
            self.tablayout.addTab(Shelf(),"test_{0}".format(i))
        self.layout.addWidget(self.tablayout)

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        if self.height() > self.width():
            self.tablayout.setTabPosition(QtGui.QTabWidget.West)
        else:
            self.tablayout.setTabPosition(QtGui.QTabWidget.North)


class FlowLayout(QtGui.QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setMargin(margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QtGui.QSizePolicy.PushButton, QtGui.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QtGui.QSizePolicy.PushButton, QtGui.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()



app = QtGui.QApplication(sys.argv)
a = Test()#QtGui.QTabWidget()
a.show()

app.exec_()

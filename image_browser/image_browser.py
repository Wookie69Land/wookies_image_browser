from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QScrollArea, QMessageBox, QMainWindow, QFileDialog
    
from actions import openAction, printAction, exitAction, zoomInAction, zoomOutAction, defaultSizeAction, fitToWindowAction, \
    aboutAction, aboutQtAction, cropImageAction, rotateLeftAction, rotateRightAction, saveImageAction
from menu import create_menu
from toolbars import create_toolbar
from imagelabel import customImageLabel
from mousetracker import MouseTracker

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = customImageLabel(self)
        self.imageLabel.setMouseTracking(True)
        self.imageLabel.installEventFilter(self)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()
        self.addToolBar(create_toolbar(self))
        
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Miłej zabawy")
        
        tracker = MouseTracker(self.imageLabel)
        tracker.positionChanged.connect(self.on_positionChanged)

        self.setWindowTitle("Wookie's Image Viewer")
        self.resize(800, 600)

    def open(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.image = image
            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.imageLabel.resize(self.imageLabel.pixmap().size())
            self.imageLabel.setAlignment(Qt.AlignCenter)

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.normalSizeAct.setEnabled(True)
            self.cropAct.setEnabled(True)
            self.rotateRightAct.setEnabled(True)
            self.rotateLeftAct.setEnabled(True)
            self.printAct.setEnabled(True)
            self.saveAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.75)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About",
                          "<p>The <b>Wookie's Image Viewer</b> is an exercise on how to create simple UID app "
                          "using Python and PyQT5 library.</p>"
                          "<p>You can find your image on your disc and display it, crop it and print it.</p>")

    def createActions(self):
        self.openAct = openAction(self)
        self.printAct = printAction(self)
        self.saveAct = saveImageAction(self)
        self.exitAct = exitAction(self)
        self.zoomInAct = zoomInAction(self)
        self.zoomOutAct = zoomOutAction(self)
        self.normalSizeAct = defaultSizeAction(self)
        self.fitToWindowAct = fitToWindowAction(self)
        self.cropAct = cropImageAction(self)
        self.rotateRightAct = rotateRightAction(self)
        self.rotateLeftAct = rotateLeftAction(self)
        self.aboutAct = aboutAction(self)
        self.aboutQtAct = aboutQtAction(self)

    def createMenus(self):
        create_menu(self)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        """Zoom in and zoom out."""
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())
        
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)
        
        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)
        
        self.updateActions()

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))
    
    @pyqtSlot(QPoint)
    def on_positionChanged(self, pos):
        self.statusbar.showMessage(f"Mouse Coordinates: ({pos.x()}, {pos.y()})")
        
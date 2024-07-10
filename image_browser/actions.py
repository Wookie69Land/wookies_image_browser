from pathlib import Path

from PyQt5.QtWidgets import QAction, QMainWindow, qApp
from PyQt5.QtGui import QIcon

from imagelabel import customImageLabel


PATH_TO_ICONS = str(Path(__file__).parent) + '\\icons\\'


def openAction(window: QMainWindow):
    return QAction(QIcon(PATH_TO_ICONS + "open.png"), 
                   "&Open...", window, shortcut="Ctrl+O", triggered=window.open)

def printAction(window: QMainWindow):
    return QAction(QIcon(PATH_TO_ICONS + "print.png"), 
                   "&Print...", window, shortcut="Ctrl+P", enabled=False, triggered=window.print_)

def exitAction(window: QMainWindow):
    return QAction(QIcon(PATH_TO_ICONS + "exit.png"), 
                   "E&xit", window, shortcut="Ctrl+Q", triggered=window.close)

def zoomInAction(window: QMainWindow):
    return QAction(QIcon(PATH_TO_ICONS + "zoom_in.png"), 
                   "Zoom &In (25%)", window, shortcut="Ctrl++", enabled=False, triggered=window.zoomIn)

def zoomOutAction(window: QMainWindow):
    return QAction(QIcon(PATH_TO_ICONS + "zoom_out.png"), 
                   "Zoom &Out (25%)", window, shortcut="Ctrl+-", enabled=False, triggered=window.zoomOut)

def defaultSizeAction(window: QMainWindow):
    return QAction("&Normal Size", window, shortcut="Ctrl+S", enabled=False, triggered=window.normalSize)

def fitToWindowAction(window: QMainWindow):
    return QAction("&Fit to Window", window, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=window.fitToWindow)
    
def aboutAction(window: QMainWindow):
    return QAction("&About", window, triggered=window.about)

def aboutQtAction(window: QMainWindow):
    return QAction("About &Qt", window, triggered=qApp.aboutQt)

def saveImageAction(window: QMainWindow):
    saveAction = QAction("&Save as", window, enabled=False, shortcut="Ctrl+S")
    saveAction.triggered.connect(lambda: window.imageLabel.saveImage())
    return saveAction
    
def rotateRightAction(window: QMainWindow):
    rotateRightAction = QAction(QIcon(PATH_TO_ICONS + "rotate90_cw.png"), "Rotate &right", window, 
                                enabled=False, shortcut="Ctrl+6")
    rotateRightAction.triggered.connect(lambda: window.imageLabel.rotateImage90('cw'))
    return rotateRightAction

def rotateLeftAction(window: QMainWindow):
    rotateLeftAction = QAction(QIcon(PATH_TO_ICONS + "rotate90_ccw.png"), "Rotate &left", window, 
                               enabled=False, shortcut="Ctrl+4")
    rotateLeftAction.triggered.connect(lambda: window.imageLabel.rotateImage90('ccw'))
    return rotateLeftAction

def cropImageAction(window: QMainWindow):
    cropAction = QAction(QIcon(PATH_TO_ICONS + "crop.png"), "&Crop", window, enabled=False)
    cropAction.setShortcut('Ctrl+C')
    cropAction.triggered.connect(lambda: window.imageLabel.cropImage)
    return cropAction

def mouseMoveAction(windows: QMainWindow):
    #TODO implement tracking mouse move
    pass

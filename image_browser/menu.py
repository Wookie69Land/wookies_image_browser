from PyQt5.QtWidgets import QMenu, QMainWindow

def create_menu(window: QMainWindow):
    window.fileMenu = QMenu("&File", window)
    window.fileMenu.addAction(window.openAct)
    window.fileMenu.addAction(window.printAct)
    window.fileMenu.addAction(window.saveAct)
    window.fileMenu.addSeparator()
    window.fileMenu.addAction(window.exitAct)
    
    window.viewMenu = QMenu("&View", window)
    window.viewMenu.addAction(window.zoomInAct)
    window.viewMenu.addAction(window.zoomOutAct)
    window.viewMenu.addAction(window.normalSizeAct)
    window.viewMenu.addSeparator()
    window.viewMenu.addAction(window.fitToWindowAct)
    
    window.editMenu = QMenu("&Edit", window)
    window.editMenu.addAction(window.cropAct)
    window.editMenu.addSeparator()
    window.editMenu.addAction(window.rotateRightAct)
    window.editMenu.addAction(window.rotateLeftAct)
    
    window.helpMenu = QMenu("&Help", window)
    window.helpMenu.addAction(window.aboutAct)
    window.helpMenu.addAction(window.aboutQtAct)
    
    window.menuBar().addMenu(window.fileMenu)
    window.menuBar().addMenu(window.viewMenu)
    window.menuBar().addMenu(window.editMenu)
    window.menuBar().addMenu(window.helpMenu)
    
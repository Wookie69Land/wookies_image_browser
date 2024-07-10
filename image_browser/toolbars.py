from PyQt5.QtWidgets import QToolBar, QMainWindow
from PyQt5.QtCore import QSize


def create_toolbar(window: QMainWindow):
    TOOL_BAR_STYLE = """
        QToolBar {
            background-color: light grey;
            spacing: 4px;
        }
        QToolBar QToolButton {
            color: black;
        }
    """
    simpleToolbar = QToolBar("Roll", window)
    simpleToolbar.setStyleSheet(TOOL_BAR_STYLE)
    simpleToolbar.addAction(window.openAct)
    simpleToolbar.addAction(window.printAct)
    simpleToolbar.addSeparator()
    simpleToolbar.addAction(window.zoomInAct)
    simpleToolbar.addAction(window.zoomOutAct)
    simpleToolbar.addSeparator()
    simpleToolbar.addAction(window.cropAct)
    simpleToolbar.addAction(window.rotateRightAct)
    simpleToolbar.addAction(window.rotateLeftAct)
    simpleToolbar.addSeparator()
    simpleToolbar.addAction(window.exitAct)
    
    simpleToolbar.setIconSize(QSize(36, 36))
    
    return simpleToolbar    
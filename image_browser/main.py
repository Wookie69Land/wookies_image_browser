

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from image_browser import QImageViewer

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())

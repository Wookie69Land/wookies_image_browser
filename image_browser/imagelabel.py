from PyQt5.QtWidgets import QLabel, QMessageBox, QFileDialog, QSizePolicy, QRubberBand
from PyQt5.QtCore import Qt, QSize, QRect, QEvent
from PyQt5.QtGui import QPixmap, QImage, QTransform, qRgb, QColor, QPalette


class customImageLabel(QLabel):
    """Subclass of QLabel for displaying image"""
    def __init__(self, parent, image=None):
        super().__init__(parent)
        self.parent = parent 
        self.image = image

        self.rubber_band = None
        self.originQPoint = None

        self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setScaledContents(True)
    
    def saveImage(self):
        """Save the image displayed in the label."""
        if self.image:
            image_file, _ = QFileDialog.getSaveFileName(self, "Save Image", 
                "", "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files (*.bmp);;\
                    GIF Files (*.gif)")

            if image_file and self.image:
                self.image.save(image_file)
            else:
                QMessageBox.information(self, "Error", 
                    "Unable to save image.", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Empty Image", 
                    "There is no image to save.", QMessageBox.Ok)

    def resizeImage(self):
        """Resize image."""
        #TODO: Resize image by specified size
        if self.image:
            resize = QTransform().scale(0.5, 0.5)

            pixmap = QPixmap(self.image)

            resized_image = pixmap.transformed(resize, mode=Qt.SmoothTransformation)
            #rotated = pixmap.trueMatrix(transform90, pixmap.width, pixmap.height)

            #self.image_label.setPixmap(rotated)
            
            #self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QImage(resized_image) 
            self.setPixmap(resized_image)
            #self.image = QPixmap(rotated)
            self.setScaledContents(True)
            self.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def cropImage(self):
        """Crop selected portions in the image."""
        if self.image:
            rect = QRect(10, 20, 400, 200)
            original_image = self.image
            cropped = original_image.copy(rect)

            self.image = QImage(cropped)
            self.setPixmap(QPixmap().fromImage(cropped))

    def rotateImage90(self, direction):
        """Rotate image 90º clockwise or counterclockwise."""
        if self.image:
            if direction == "cw":
                transform90 = QTransform().rotate(90)
            elif direction == "ccw":
                transform90 = QTransform().rotate(-90)

            pixmap = QPixmap(self.image)

            #TODO: Try flipping the height/width when flipping the image

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)
            self.resize(self.image.height(), self.image.width())

            self.image = QImage(rotated) 
            self.setPixmap(rotated.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            self.repaint()
        else:
            # No image to rotate
            pass

    def flipImage(self, axis):
        """
        Mirror the image across the horizontal axis.
        """
        if self.image:
            if axis == "horizontal":
                flip_h = QTransform().scale(-1, 1)
                pixmap = QPixmap(self.image)
                flipped = pixmap.transformed(flip_h)
            elif axis == "vertical":
                flip_v = QTransform().scale(1, -1)
                pixmap = QPixmap(self.image)
                flipped = pixmap.transformed(flip_v)

            self.image = QImage(flipped)
            self.setPixmap(flipped)
            self.repaint()
        else:
            # No image to flip
            pass

    def convertToGray(self):
        """Convert image to grayscale."""
        if self.image:
            converted_img = self.image.convertToFormat(QImage.Format_Grayscale16)
            self.image = QImage(converted_img)
            self.setPixmap(QPixmap().fromImage(converted_img))
            self.repaint()

    def convertToRGB(self):
        """Convert image to RGB format."""
        if self.image:
            converted_img = self.image.convertToFormat(QImage.Format_RGB32)
            self.image = QImage(converted_img)
            self.setPixmap(QPixmap().fromImage(converted_img))
            self.repaint()

    def convertToSepia(self):
        """Convert image to sepia filter."""
        #TODO: Sepia #704214 rgb(112, 66, 20)
        if self.image:
            for row_pixel in range(self.image.width()):
                for col_pixel in range(self.image.height()):
                    current_val = QColor(self.image.pixel(row_pixel, col_pixel))
            
                    # Calculate r, g, b values for current pixel
                    red = current_val.red()
                    green = current_val.green()
                    blue = current_val.blue()

                    new_red = int(0.393 * red + 0.769 * green + 0.189 * blue)
                    new_green = int(0.349 * red + 0.686 * green + 0.168 * blue)
                    new_blue = int(0.272 * red + 0.534 * green + 0.131 * blue)

                    # Set the new RGB values for the current pixel
                    if new_red > 255:
                        red = 255
                    else:
                        red = new_red

                    if new_green > 255:
                        green = 255
                    else:
                        green = new_green

                    if new_blue > 255:
                        blue = 255
                    else:
                        blue = new_blue

                    new_value = qRgb(red, green, blue)
                    self.image.setPixel(row_pixel, col_pixel, new_value)

        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()
    
    def changeBrighteness(self, value):
        #TODO: Reset the value of brightness, remember the original values 
        # as going back to 0, i.e. keep track of original image's values
        #TODO: modify values based on original image
        if (value < -255 | value > 255):
            return self.image

        for row_pixel in range(self.image.width()):
            for col_pixel in range(self.image.height()):
                current_val = QColor(self.image.pixel(row_pixel, col_pixel))
                red = current_val.red()
                green = current_val.green()
                blue = current_val.blue()

                new_red = red + value
                new_green = green + value
                new_blue = blue + value

                # Set the new RGB values for the current pixel
                if new_red > 255:
                    red = 255
                elif new_red < 0:
                    red = 0
                else:
                    red = new_red

                if new_green > 255:
                    green = 255
                elif new_green < 0:
                    green = 0
                else:
                    green = new_green

                if new_blue > 255:
                    blue = 255
                elif new_blue < 0:
                    blue = 0
                else:
                    blue = new_blue

                new_value = qRgb(red, green, blue)
                self.image.setPixel(row_pixel, col_pixel, new_value)

        self.setPixmap(QPixmap().fromImage(self.image))

    def changeContrast(self, contrast):
        """Change the contrast of the pixels in the image.
           Contrast is the difference between max and min pixel intensity."""
        for row_pixel in range(self.image.width()):
            for col_pixel in range(self.image.height()):
                # Calculate a contrast correction factor
                factor = float(259 * (contrast + 255) / (255 * (259 - contrast)))
                
                current_val = QColor(self.image.pixel(row_pixel, col_pixel))
                red = current_val.red()
                green = current_val.green()
                blue = current_val.blue()

                new_red = factor * (red - 128) + 128
                new_green = factor * (green - 128) + 128
                new_blue = factor * (blue - 128) + 128

                new_value = qRgb(new_red, new_green, new_blue)
                self.image.setPixel(row_pixel, col_pixel, new_value)

        self.setPixmap(QPixmap().fromImage(self.image))

    def changeHue(self):
        for row_pixel in range(self.image.width()):
            for col_pixel in range(self.image.height()):
                current_val = QColor(self.image.pixel(row_pixel, col_pixel))

                hue = current_val.hue()

                current_val.setHsv(hue, current_val.saturation(), 
                        current_val.value(), current_val.alpha())
                self.image.setPixelColor(row_pixel, col_pixel, current_val)

        self.setPixmap(QPixmap().fromImage(self.image))

    def mousePressEvent(self, eventQMouseEvent):
        if not self.rubber_band:
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.originQPoint = eventQMouseEvent.pos()
        self.rubber_band.setGeometry(QRect(self.originQPoint, QSize()))
        self.rubber_band.show()

    def mouseMoveEvent(self, eventQMouseEvent):
        if self.originQPoint:
            self.rubber_band.setGeometry(QRect(self.originQPoint, eventQMouseEvent.pos()).normalized() & self.rect())

    def mouseReleaseEvent (self, eventQMouseEvent):
        self.rubber_band.hide()
        currentQRect = self.rubber_band.geometry()
        # self.rubber_band.deleteLater()
        cropped_image = self.pixmap().copy(currentQRect)
        self.setPixmap(cropped_image)
        # cropped_image.save('output.png')



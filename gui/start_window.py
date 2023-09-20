from filtering_window import FilteringWindow
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


class StartWindow(QWidget):
    """
    Starting window that welcomes user and opens the filtering window
    """
    def __init__(self):
        super().__init__()

        # Create filtering window
        self.filter_window = FilteringWindow()
        self.setWindowTitle("ClassMate")
        self.setStyleSheet("background-color: darkcyan;")
        layout = QHBoxLayout()

        layout_v = QVBoxLayout()
        lbl = QLabel('Welcome to Classmate')
        font = lbl.font()
        font.setPointSize(30)
        lbl.setFont(font)
        lbl.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        button1 = QPushButton("Get Started")
        button1.clicked.connect(self.toggle_filter_window)
        layout_v.addWidget(lbl)
        layout_v.addWidget(button1, alignment=Qt.AlignTop)

        pic = QLabel()
        image = QPixmap('C:\\Users\\thpap\\PycharmProjects\\ClassMate\\Ucla_Pic.jpg')
        pixmap_resized = image.scaled(512, 512, Qt.KeepAspectRatio)
        pic.setPixmap(pixmap_resized)

        # pic.setScaledContents(True)
        layout.addLayout(layout_v)
        layout.addWidget(pic)

        self.setLayout(layout)
        self.show()
        self.showFullScreen()

    def toggle_filter_window(self, checked) -> None:
        """
        toggles filtering window if it is not visible
        :param checked: whether button is checked or not
        :return: None
        """
        if self.filter_window.isVisible():
            self.filter_window.hide()
        else:
            self.filter_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = StartWindow()
    w.show()
    app.exec()

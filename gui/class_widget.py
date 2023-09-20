from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QMainWindow, QVBoxLayout, QSizePolicy, QApplication
from PyQt5.QtCore import Qt
import random as rng
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Color(QWidget):
    """
    class that changes the palette color of a widget
    """
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)


class ClassBox(QWidget):
    """
    Custom Qt Widget to display the class in a box with a minus/ plus sign
    depending on use and a label to indicate match percentage
    """
    buttonClicked = QtCore.pyqtSignal(QWidget)
    classClicked = QtCore.pyqtSignal(QWidget)

    def __init__(self, class_name: str, class_details: dict, parent: QMainWindow = None):
        super(ClassBox, self).__init__()

        self.setParent(parent)
        self.class_details = class_details
        self.course_name = class_name
        self.plus = True
        self.ai_toggle = True
        self.score = 0

        # Generates random background color
        self.rgb_color = (rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255))

        # Creates widget layout
        # self.setFixedSize(200, 100)
        layout = QVBoxLayout()
        self.lbl = self.name_label()
        self.lbl.clicked.connect(self.onLabelClicked)

        self.btn = self.button()
        self.match_lbl = self.match_percent()
        layout.addWidget(self.lbl)
        self.setLayout(layout)

        self.generate_random_schedule()

    def name_label(self) -> QPushButton:
        """
        Creates label (actually button) that has the name of the course
        :return: parent button that has course name
        """
        label = QPushButton(self.class_name, self)
        label.setCheckable(False)
        label.setAutoDefault(False)

        # label = QtWidgets.QLabel(self.class_name)
        # sets style of button
        label.setStyleSheet(f'''border-radius : 5px;
                                border: 2px solid black;
                                background-color:rgb({self.rgb_color[0]},{self.rgb_color[1]},{self.rgb_color[2]})
                                ''')

        # fixes text and geometry of button (NEEDS FIXING)
        font = label.font()
        font.setPointSize(5)
        label.setGeometry(0, 0, 145, 80)
        # label.setFixedSize(170, 80)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        label.setMinimumSize(80, 80)
        label.setMaximumSize(170, 80)
        label.setFont(font)
        # label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        return label

    def button(self) -> QPushButton:
        """
        Creates plus or minus icon button
        :return: plus/ minus icon button
        """

        # creating a push button
        button = QPushButton('', self.lbl)

        if self.plus:
            button.setIcon(QtGui.QIcon('plus-circle.png'))
        else:
            button.setIcon(QtGui.QIcon('minus-circle.png'))

        # Fixes size and position of button (NEEDS FIXING)
        button.setIconSize(QtCore.QSize(20, 20))
        # button.setGeometry(QtCore.QRect(50, 25, 100, 50))
        # button.setFixedSize(20, 20)
        btn_pos = self.lbl.geometry().topRight()
        button.move(btn_pos)

        button.clicked.connect(self.onButtonClicked)

        return button

    def match_percent(self) -> QLabel:
        """
        Label that displays how closely a course option matches the user
        :param percentage: match percentage
        :return: None
        """
        label = QLabel(f'score: {self.score}', self.lbl)
        label.setStyleSheet('''border-radius : 1px;
                                        border: 1px solid black''')
        font = label.font()
        font.setPointSize(5)
        label.resize(50, 20)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        percentage_lbl_pos_x = self.lbl.geometry().center() + QtCore.QPoint(-label.geometry().right()//4, self.lbl.geometry().bottom()//2 - label.geometry().bottom())
        label.move(percentage_lbl_pos_x)
        label.setVisible(self.ai_toggle)

        return label

    def generate_random_schedule(self) -> None:
        """
        Generates a random time schedule for the class
        :return: None
        """

        # possible lecture days
        days = ["MW", "TT", "WF", "Mo", "Tu", "We", "Th", "Fr"]

        # selects random, hours, duration and days
        hours = list(range(1, 8))
        duration = rng.randint(1, 3)
        start_hour = rng.choice(hours)
        day = rng.choice(days)
        finish_hour = start_hour + duration

        # add it in class details
        self.class_details['Schedule'] = (day, start_hour, finish_hour)

    def onButtonClicked(self) -> None:
        """
        Emits signal on buttonpress so that the event can be intercepted by parent window
        :return: None
        """
        self.buttonClicked.emit(self)

    def change_button(self) -> None:
        """
        Changes button between plus/minus icons
        :return: None
        """
        self.plus = not self.plus
        if self.plus:
            self.btn.setIcon(QtGui.QIcon('plus-circle.png'))
        else:
            self.btn.setIcon(QtGui.QIcon('minus-circle.png'))
    
    def set_percentage(self, score: int):
        self.score = score
        self.match_lbl.setText(f'score: {self.score}')

    def onLabelClicked(self) -> None:
        """
        Opens the hyperlink of the class website on click on the label of the course
        :return: None
        """
        # chr_options = Options()
        # chr_options.add_experimental_option("detach", True)
        # driver = webdriver.Chrome(options=chr_options)
        # driver.get(self.class_details['href'])

        self.classClicked.emit(self)

    @property
    def color(self):
        return self.rgb_color

    @property
    def class_name(self):
        return self.course_name


if __name__ == "__main__":
    app = QApplication([])
    volume = ClassBox('peaki o roubis o koumpis o roumpokompologis', {})
    volume.show()
    app.exec_()

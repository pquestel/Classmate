import numpy as np

from class_widget import ClassBox
from constraint_filtering import ConstraintBasedFilter
from calendar_widget import CalendarWidget
from start_window import StartWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
from statics import load_dict_from_json
import os
from text_filter import TextFilter


class MainWindow(QMainWindow):
    """
    Main window that has the recommendation results of the AI, and enable addition of classes to interactive calendar
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        # creates Start window that welcome user (User login in that page in the future)
        self.start_window = StartWindow()
        self.setWindowTitle("ClassMate")
        self.setVisible(False)
        self.start_window.filter_window.submit_button.clicked.connect(self.load_main_window)

        self.create_menu()

        self.course_dict = {}
        self.course_widgets = []
        self.display_course_widget_indexes = []

        self.calendar_widget = CalendarWidget(self)

        self.text_box = QPlainTextEdit(self)
        self.text_display = QPlainTextEdit(self)

        self.prompt_enter_btn = QPushButton('Enter text')
        self.prompt_enter_btn.clicked.connect(self.input_prompt)

        self.webview = QWebEngineView(self)
        self.webview.setFixedSize(1050, 600)

        self.recommendations_widget = QTableWidget(3, 50)
        # self.recommendations_widget.setGeometry(50, 200, self.calendar_widget.width(), self.calendar_widget.height())

        self.text_filter = TextFilter()
        self.constraint_based_filter = ConstraintBasedFilter()

    def load_courses(self):
        self._load_course_dict()
        self.course_widgets = np.array([ClassBox(class_name, self.course_dict[class_name])
                                        for class_name in list(self.course_dict.keys())])
        self.display_course_widget_indexes = list(range(len(self.course_widgets)))

    def _load_course_dict(self) -> None:
        """
        Loads class details from the course_data.json generated from the webscrapping script
        :return: None
        """
        self.course_dict = load_dict_from_json(os.path.join(os.pardir, "course_data.json"))

    def _hide_other_windows(self) -> None:
        """
        Hides the starting and filtering windows
        :return: None
        """
        if self.start_window.isVisible():
            self.start_window.hide()
        if self.start_window.filter_window.isVisible():
            self.start_window.filter_window.hide()

    def load_main_window(self):
        """
        Gets the results of the filtering window, creates the constraint based filtering
         and loads the class and calendar widgets
        :return: None
        """

        # gets constraints from filtering window
        constraints = self.start_window.filter_window.on_submit_button_clicked()
        self.constraint_based_filter.update_constraints(constraints)

        self.load_courses()

        self.constraint_filter_widgets()
        self.text_filter_widgets('')
        self.update_recommended_classes()

        self.form_window_layout()

    def form_window_layout(self):
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        self.text_box.setGeometry(50, 50, 100, 150)
        self.text_box.setPlaceholderText("Enter your prompt here:")

        self.text_display.setGeometry(50, 50, 100, 150)
        self.text_display.setPlainText("LLM conversation:\n")
        self.text_display.setReadOnly(True)
        self.text_display.setCenterOnScroll(True)

        bottom_layout.addWidget(self.calendar_widget)
        bottom_layout.addWidget(self.text_box)
        bottom_layout.addWidget(self.text_display)
        bottom_layout.addWidget(self.prompt_enter_btn)

        top_layout.addWidget(self.recommendations_widget)
        top_layout.addWidget(self.webview)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setVisible(True)
        self.showFullScreen()
        self._hide_other_windows()

    def onClassButtonClicked(self, class_box_widget: ClassBox) -> None:
        """
        Adds class to calendar view when the plus button is presses and removes it when minus button is clicked.
        It also changes between minus/ plus icons
        :param class_box_widget: classbox widget for which the action happens
        :return: None
        """

        if class_box_widget.plus:
            self.calendar_widget.courses.append(class_box_widget)
            self.calendar_widget.populate_calendar()
        else:
            self.calendar_widget.courses.remove(class_box_widget)
            self.calendar_widget.clear()
            self.calendar_widget.draw_empty_table()
            self.calendar_widget.populate_calendar()
        class_box_widget.change_button()

    def create_menu(self) -> None:
        """
        Creates menu bar with Quit option to quit the full-screen application
        :return: None
        """
        # Create a menu bar
        menubar = self.menuBar()

        # Create a "File" menu
        file_menu = menubar.addMenu("&Quit ClassMate")

        # Create a "Quit" action
        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)
        quit_action.triggered.connect(QApplication.quit)

        # Add the "Quit" action to the "File" menu
        file_menu.addAction(quit_action)

    def input_prompt(self):

        self.text_display.appendPlainText('You said: \n' + self.text_box.toPlainText())
        self.text_display.appendPlainText('AI replied: \n' + 'peaki' + '\n')
        self.text_display.ensureCursorVisible()

        self.text_filter_widgets(self.text_box.toPlainText())

        self.text_box.clear()

        self.update_recommended_classes()

    def constraint_filter_widgets(self):
        constraint_filtered_indexes = []
        for index, class_widget in enumerate(self.course_widgets):
            if self.constraint_based_filter.filter_course(class_widget.class_details):
                class_widget.buttonClicked.connect(self.onClassButtonClicked)
                class_widget.classClicked.connect(self.update_webview)
                constraint_filtered_indexes.append(index)
        self.display_course_widget_indexes = constraint_filtered_indexes

    def text_filter_widgets(self, text_prompt):

        text_filtered_widget_indexes = []
        self.text_filter.extract_keywords(text_prompt)

        # Text Filtering
        if text_prompt != '' and text_prompt != 'Enter your prompt here:':
            print('no prompt')
            for class_index in self.display_course_widget_indexes:
                if self.text_filter.rank_classes(self.course_widgets[class_index]):
                    text_filtered_widget_indexes.append(class_index)

            self.display_course_widget_indexes = text_filtered_widget_indexes
            self.display_course_widget_indexes.sort(reverse=True, key=lambda x: self.course_widgets[x].score)

        self.display_course_widget_indexes = list(range(len(self.course_widgets)))

    def update_recommended_classes(self):
        print(self.display_course_widget_indexes)
        i = 0
        # self.recommendations_widget.clearContents()
        for col in range(self.recommendations_widget.columnCount()):
            for row in range(self.recommendations_widget.rowCount()):
                if i >= len(self.display_course_widget_indexes):
                    break
                table_item = QTableWidgetItem()
                self.recommendations_widget.setCellWidget(row, col,
                                                          self.course_widgets[self.display_course_widget_indexes[i]])
                self.recommendations_widget.setItem(row, col, table_item)
                self.recommendations_widget.setColumnWidth(col, 300)
                self.recommendations_widget.setRowHeight(row, 150)
                i += 1

    def update_webview(self, class_box_widget: ClassBox) -> None:

        # Load a website
        self.webview.setUrl(QUrl(class_box_widget.class_details['href']))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()

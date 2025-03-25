###############################################################################################
# Tytuł: SCADA
# Autor: Jakub Kalamaszek
# Data: 10.03.2025
# Wersja: v.0.0.1
# Scieżka: C:\Users\Kuba\OneDrive\Pulpit\2 stopień\sem10\Praca Magisterska
###############################################################################################

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeView, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QLabel, QDialog, QSpinBox, QDoubleSpinBox, QPushButton, QScrollArea, QGroupBox, QLineEdit, QMessageBox, QComboBox, \
    QCheckBox, QProgressBar, QCalendarWidget, QSizePolicy, QButtonGroup, QFontComboBox, QDateEdit, QColorDialog, QFrame,\
    QSlider
from PyQt6.QtGui import QAction, QFileSystemModel, QFont
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QBrush, QColor, QPen
import sys
import os
import generic_functions as generic
from LoggingModule import log_manager
from ErrorModule import ErrorMSG
from datetime import date

# Set base directory
BASEDIR = os.path.dirname(__file__)


class DottedWidget(QWidget):
    def __init__(self):
        super(DottedWidget, self).__init__()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        for x in range(0, self.width(), 10):
            for y in range(0, self.height(), 10):
                painter.drawEllipse(x, y, 1, 1)


class CircleWidget(QWidget):
    def __init__(self, x=50, y=50, diameter=100, color=QColor(0, 0, 255), filled=True, object_name='Circle', width=100, height=100, parent=None):
        super().__init__(parent)
        self.circle_x = x
        self.circle_y = y
        self.width = width
        self.height = height
        self.circle_diameter = diameter
        self.circle_color = color
        self.filled = filled  # Czy środek koła ma być wypełniony?
        self.setMinimumSize(400, 400)
        self.setObjectName(object_name)
        self.show_red_border = False  # Domyślnie ramka wyłączona
        self.show_green_border = False  # Domyślnie ramka wyłączona

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Tworzymy pędzel i ustawiamy kolor
        brush = QBrush(self.circle_color, Qt.BrushStyle.SolidPattern if self.filled else Qt.BrushStyle.NoBrush)
        painter.setBrush(brush)

        # Tworzymy obrys
        pen = QPen(self.circle_color)  # Czarny obrys
        pen.setWidth(2)
        painter.setPen(pen)

        # Rysowanie koła
        painter.drawEllipse(self.circle_x, self.circle_y, self.circle_diameter, self.circle_diameter)

        if self.show_red_border:  # Sprawdzenie, czy ramka ma być rysowana
            self.draw_red_border(painter)
        if self.show_green_border:  # Sprawdzenie, czy ramka ma być rysowana
            self.draw_green_border(painter)

    def draw_red_border(self, painter):
        border_pen = QPen(QColor(255, 0, 0))  # Czerwony kolor
        border_pen.setWidth(1)  # Grubość ramki
        painter.setPen(border_pen)

        painter.drawEllipse(self.circle_x, self.circle_y, self.circle_diameter, self.circle_diameter)

    def draw_green_border(self, painter):
        border_pen = QPen(QColor(124, 252, 0))  # Zielony kolor
        border_pen.setWidth(1)  # Grubość ramki
        painter.setPen(border_pen)

        painter.drawEllipse(self.circle_x, self.circle_y, self.circle_diameter, self.circle_diameter)

    def toggle_red_border(self):
        """Metoda do przełączania czerwonej ramki"""
        self.show_red_border = True  # Przełączanie wartości
        self.update()  # Wymuszenie ponownego rysowania

    def toggle_green_border(self):
        """Metoda do przełączania zielonej ramki"""
        self.show_green_border = True  # Przełączanie wartości
        self.update()  # Wymuszenie ponownego rysowania

    def hide_red_border(self):
        self.show_red_border = False
        self.update()

    def hide_green_border(self):
        self.show_green_border = False
        self.update()


class RectangleWidget(QWidget):
    def __init__(self, x=50, y=50, width=150, height=100, color=QColor(0, 255, 0), filled=True, object_name='Rectangle', parent=None):
        super().__init__(parent)
        self.rect_x = x
        self.rect_y = y
        self.rect_width = width
        self.rect_height = height
        self.rect_color = color
        self.filled = filled  # Czy prostokąt ma być wypełniony?
        self.setMinimumSize(400, 400)
        self.setObjectName(object_name)
        self.show_red_border = False  # Domyślnie ramka wyłączona

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Tworzymy pędzel i ustawiamy kolor
        brush = QBrush(self.rect_color, Qt.BrushStyle.SolidPattern if self.filled else Qt.BrushStyle.NoBrush)
        painter.setBrush(brush)

        # Tworzymy obrys
        pen = QPen(self.rect_color)  # Czarny obrys
        pen.setWidth(2)
        painter.setPen(pen)

        # Rysowanie prostokąta
        painter.drawRect(self.rect_x, self.rect_y, self.rect_width, self.rect_height)

        if self.show_red_border:  # Sprawdzenie, czy ramka ma być rysowana
            self.draw_red_border(painter)

    def draw_red_border(self, painter):
        border_pen = QPen(QColor(255, 0, 0))  # Czerwony kolor
        border_pen.setWidth(1)  # Grubość ramki
        painter.setPen(border_pen)

        # Rysowanie prostokąta otaczającego koło
        painter.drawRect(self.rect_x, self.rect_y, self.rect_width, self.rect_height)

    def toggle_red_border(self):
        """Metoda do przełączania czerwonej ramki"""
        self.show_red_border = True  # Przełączanie wartości
        self.update()  # Wymuszenie ponownego rysowania

    def hide_red_border(self):
        self.show_red_border = False
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    # interfejs użytkownika
    def init_ui(self):
        self.setWindowTitle("SCADA System")

        # parametry wstępne
        self.screen_width = self.get_screen_width()
        self.screen_height = self.get_screen_height()
        self.tree_view_width = int(self.screen_width/7)
        self.widgets_bar_width = int(self.screen_width/6)
        self.widget_parameter_bar_width = int(self.screen_width/6)
        self.root_space_width = self.screen_width - self.tree_view_width - self.widgets_bar_width - self.widget_parameter_bar_width
        self.low_margine = 49
        self.menu_bar_height_margine = 55
        self.status_bar_height = 30
        self.window_height = int(self.screen_height - self.low_margine - self.status_bar_height - self.menu_bar_height_margine)
        self.upper_limit = 33
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.init_menu()

        # Utworzenie drzewka nawigacji
        self.create_tree_view()

        # Utworzenie paska stanu
        self.status_bar = self.statusBar()
        self.status_bar.setFixedHeight(self.status_bar_height)
        self.status_bar.setStyleSheet("background-color: #444; color: white;")

        # Utworzenie przestrzni roboczej
        self.root_space()

        # Utworzenie paska widgetów
        self.widgets_bar()

        # Utworzenie paska parametrów widgetó
        self.widget_parameter_bar()

        self.show()

        # Timer do śledzenia położenia kursora
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_cursor_position)
        self.timer.start(50)  # aktualizacja co 50 ms

    # szerokość okna
    def get_screen_width(self):
        return QApplication.primaryScreen().size().width()

    # wysokość okna
    def get_screen_height(self):
        return QApplication.primaryScreen().size().height()

    # menu bar
    def init_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #444; color: white;")

        file_menu = menubar.addMenu("File")
        view_menu = menubar.addMenu("View")
        help_menu = menubar.addMenu("Help")

        new_window = QAction('New Window', self)
        new_window.triggered.connect(self.new_window)
        file_menu.addAction(new_window)
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    # drzewko nawigacji
    def create_tree_view(self):
        # aktualny folder
        current_folder_path = os.getcwd()

        # Drzewo projektu
        tree_view = QTreeView(self)
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(current_folder_path)
        tree_view.setModel(self.file_system_model)
        tree_view.setRootIndex(self.file_system_model.index(current_folder_path))
        tree_view.setStyleSheet("background-color: #ADD8E6")

        # Ustawienie szerokości i wysokości drzewa projektu
        tree_view.setGeometry(0, self.upper_limit, self.tree_view_width, int(self.screen_height/2.9))

        # Ukrycie niepotrzebnych kolumn
        tree_view.setColumnHidden(1, True)
        tree_view.setColumnHidden(2, True)
        tree_view.setColumnHidden(3, True)

        # ukrycie scrolla drzewka
        tree_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # ustawienie szerokości kolumn
        tree_view.setColumnWidth(0, int(self.screen_width/10))
        tree_view.setColumnWidth(3, int(self.screen_width/8.5))

    # przestrzen robocza(na okna)
    def root_space(self):
        # stworzenie przestrzeni roboczej(ciemny prostokąt)
        self.root_space_groupbox = QGroupBox()
        self.root_space_groupbox.setFixedHeight(5000)
        self.root_space_groupbox.setFixedWidth(3000)
        self.root_space_groupbox.setStyleSheet("background-color: darkgrey; padding: 10px;")
        self.root_space_groupbox.setObjectName('root_space_groupbox')

        self.root_space_area = QScrollArea(self)
        self.root_space_area.setWidget(self.root_space_groupbox)
        self.root_space_area.setWidgetResizable(True)
        self.root_space_area.setGeometry(self.tree_view_width, self.upper_limit, self.root_space_width, self.window_height)
        self.root_space_area.setObjectName('root_space_area')

    def widget_parameter_bar(self):
        # stworzenie Scroll Area
        self.widget_parameter_box = QGroupBox()
        self.widget_parameter_box.setFixedWidth(self.widget_parameter_bar_width-15)
        self.widget_parameter_box.setFixedHeight(self.window_height + 500)
        self.widget_parameter_box.setStyleSheet("background-color: lightblue;")
        self.widget_parameter_box.setFlat(True)

        self.widget_parameter_scroll_area = QScrollArea(self)
        self.widget_parameter_scroll_area.setWidget(self.widget_parameter_box)
        self.widget_parameter_scroll_area.setWidgetResizable(True)
        self.widget_parameter_scroll_area.setGeometry(int(self.tree_view_width + self.root_space_width), self.upper_limit, self.widget_parameter_bar_width, self.window_height)
        self.widget_parameter_scroll_area.setObjectName('widget_parameter_bar_area')


        # ScrollArea 'Geometry'
        ################################################################################################################
        self.geometry_box = QGroupBox()
        self.geometry_box.setFixedWidth(self.widget_parameter_bar_width-15)
        self.geometry_box.setFixedHeight(153)
        self.geometry_box.setTitle('Geometry')
        self.geometry_box.setStyleSheet("background-color: lightblue;")

        self.geometry_area = QScrollArea(self.widget_parameter_box)
        self.geometry_area.setWidget(self.geometry_box)
        self.geometry_area.setWidgetResizable(True)
        self.geometry_area.setGeometry(0, 0, self.widget_parameter_bar_width, 155)

        # X Label
        QLabel_X = QLabel('X pos:', self.geometry_box)
        QLabel_X.setGeometry(5, 20, 100, 40)
        # X Spinbox
        self.X_pos_spinBox = QSpinBox(self.geometry_box)
        self.X_pos_spinBox.setGeometry(70, 30, 40, 20)
        self.X_pos_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.X_pos_spinBox.setMaximum(4000)
        self.X_pos_spinBox.setMinimum(0)

        # Y Label
        QLabel_Y = QLabel('Y pos:', self.geometry_box)
        QLabel_Y.setGeometry(5, 50, 100, 40)
        # Y Spinbox
        self.Y_pos_spinBox = QSpinBox(self.geometry_box)
        self.Y_pos_spinBox.setGeometry(70, 60, 40, 20)
        self.Y_pos_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.Y_pos_spinBox.setMaximum(4000)
        self.Y_pos_spinBox.setMinimum(0)

        # Width Label
        QLabel_width = QLabel('Width:', self.geometry_box)
        QLabel_width.setGeometry(5, 80, 100, 40)
        # Width Spinbox
        self.width_spinBox = QSpinBox(self.geometry_box)
        self.width_spinBox.setGeometry(70, 90, 40, 20)
        self.width_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.width_spinBox.setMaximum(4000)
        self.width_spinBox.setMinimum(0)

        # Height Label
        QLabel_height = QLabel('Height:', self.geometry_box)
        QLabel_height.setGeometry(5, 110, 100, 40)
        # Width Spinbox
        self.height_spinBox = QSpinBox(self.geometry_box)
        self.height_spinBox.setGeometry(70, 120, 40, 20)
        self.height_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.height_spinBox.setMaximum(4000)
        self.height_spinBox.setMinimum(0)
        ################################################################################################################

        # ScrollArea 'Widget Parameters'
        ################################################################################################################
        self.chosen_widget_parameters_box = QGroupBox()
        self.chosen_widget_parameters_box.setFixedWidth(self.widget_parameter_bar_width - 15)
        self.chosen_widget_parameters_box.setFixedHeight(190)
        self.chosen_widget_parameters_box.setTitle('Chosen Widget Parameters')
        self.chosen_widget_parameters_box.setStyleSheet("background-color: lightblue;")


        self.chosen_widget_parameters_area = QScrollArea(self.widget_parameter_box)
        self.chosen_widget_parameters_area.setWidget(self.chosen_widget_parameters_box)
        self.chosen_widget_parameters_area.setWidgetResizable(True)
        self.chosen_widget_parameters_area.setGeometry(0, 160, self.widget_parameter_bar_width, 192)


        # Add Widget button
        self.add_widget_button = QPushButton(self.widget_parameter_box)
        self.add_widget_button.setText('Add Widget')
        font = QFont("Arial", 10)
        self.add_widget_button.setFont(font)
        self.add_widget_button.setStyleSheet("background-color: white; padding: 0px;")
        self.add_widget_button.setGeometry(60, 360, 120, 35)
        self.add_widget_button.clicked.connect(self.add_widget_to_window)
        ################################################################################################################

        # DeleteWidgetArea
        ################################################################################################################
        self.delete_widget_box = QGroupBox()
        self.delete_widget_box.setFixedWidth(self.widget_parameter_bar_width - 15)
        self.delete_widget_box.setFixedHeight(140)
        self.delete_widget_box.setTitle('Delete Widget')

        self.delete_widget_area = QScrollArea(self.widget_parameter_box)
        self.delete_widget_area.setWidget(self.delete_widget_box)
        self.delete_widget_area.setWidgetResizable(True)
        self.delete_widget_area.setGeometry(0, 410, self.widget_parameter_bar_width, 142)

        # QLabel 'Window Name'
        label_window_name = QLabel(self.delete_widget_box)
        label_window_name.setText('Window Name:')
        font = QFont("Arial", 10)
        label_window_name.setFont(font)
        label_window_name.setGeometry(10, 20, 120, 35)
        # object name to delete ComboBox
        self.window_name_delete_comboBox = QComboBox(self.delete_widget_box)
        self.window_name_delete_comboBox.setGeometry(100, 27, 110, 20)
        font = QFont('Arial', 8)
        self.window_name_delete_comboBox.setFont(font)
        self.window_name_delete_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.window_name_delete_comboBox.currentTextChanged.connect(self.update_object_name_to_delete_comboBox)

        # QLabel 'Object Name'
        label_object_name = QLabel(self.delete_widget_box)
        label_object_name.setText('Object Name:')
        font = QFont("Arial", 10)
        label_object_name.setFont(font)
        label_object_name.setGeometry(10, 50, 120, 35)
        # object name to delete ComboBox
        self.object_name_delete_comboBox = QComboBox(self.delete_widget_box)
        self.object_name_delete_comboBox.setGeometry(100, 57, 110, 20)
        font = QFont('Arial', 8)
        self.object_name_delete_comboBox.setFont(font)
        self.object_name_delete_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.object_name_delete_comboBox.currentTextChanged.connect(self.widget_to_delete_changed)

        # Delete Widget button
        self.delete_button_button = QPushButton(self.delete_widget_box)
        self.delete_button_button.setText('Delete Widget')
        font = QFont("Arial", 10)
        self.delete_button_button.setFont(font)
        self.delete_button_button.setStyleSheet("background-color: white; padding: 0px;")
        self.delete_button_button.setGeometry(60, 90, 120, 35)
        self.delete_button_button.clicked.connect(self.delete_widget)

        # UpdateWidgetArea
        ################################################################################################################
        self.update_widget_box = QGroupBox()
        self.update_widget_box.setFixedWidth(self.widget_parameter_bar_width - 15)
        self.update_widget_box.setFixedHeight(98)
        self.update_widget_box.setTitle('Update Widget')

        self.update_widget_area = QScrollArea(self.widget_parameter_box)
        self.update_widget_area.setWidget(self.update_widget_box)
        self.update_widget_area.setWidgetResizable(True)
        self.update_widget_area.setGeometry(0, 580, self.widget_parameter_bar_width, 100)

        # QLabel 'Window Name'
        label_window_name = QLabel(self.update_widget_box)
        label_window_name.setText('Window Name:')
        font = QFont("Arial", 10)
        label_window_name.setFont(font)
        label_window_name.setGeometry(10, 20, 120, 35)
        # object name to update ComboBox
        self.window_name_update_comboBox = QComboBox(self.update_widget_box)
        self.window_name_update_comboBox.setGeometry(100, 27, 110, 20)
        font = QFont('Arial', 8)
        self.window_name_update_comboBox.setFont(font)
        self.window_name_update_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.window_name_update_comboBox.currentTextChanged.connect(self.update_object_name_to_update_comboBox)

        # QLabel 'Object Name'
        label_object_name = QLabel(self.update_widget_box)
        label_object_name.setText('Object Name:')
        font = QFont("Arial", 10)
        label_object_name.setFont(font)
        label_object_name.setGeometry(10, 50, 120, 35)
        # object name to update ComboBox
        self.object_name_update_comboBox = QComboBox(self.update_widget_box)
        self.object_name_update_comboBox.setGeometry(100, 57, 110, 20)
        font = QFont('Arial', 8)
        self.object_name_update_comboBox.setFont(font)
        self.object_name_update_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.object_name_update_comboBox.currentTextChanged.connect(self.widget_to_delete_changed)
        self.object_name_update_comboBox.currentTextChanged.connect(self.widget_to_update_changed)
        ################################################################################################################

        # ScrollArea update widget 'Geometry'
        ################################################################################################################
        self.update_widget_geometry_box = QGroupBox()
        self.update_widget_geometry_box.setFixedWidth(self.widget_parameter_bar_width - 15)
        self.update_widget_geometry_box.setFixedHeight(153)
        self.update_widget_geometry_box.setTitle('Geometry')
        self.update_widget_geometry_box.setStyleSheet("background-color: lightblue;")

        self.update_widget_geometry_area = QScrollArea(self.widget_parameter_box)
        self.update_widget_geometry_area.setWidget(self.update_widget_geometry_box)
        self.update_widget_geometry_area.setWidgetResizable(True)
        self.update_widget_geometry_area.setGeometry(0, 680, self.widget_parameter_bar_width, 155)

        # X Label
        QLabel_X = QLabel('X pos:', self.update_widget_geometry_box)
        QLabel_X.setGeometry(5, 20, 100, 40)
        # X Spinbox
        self.X_pos_update_spinBox = QSpinBox(self.update_widget_geometry_box)
        self.X_pos_update_spinBox.setGeometry(70, 30, 40, 20)
        self.X_pos_update_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.X_pos_update_spinBox.setMaximum(4000)
        self.X_pos_update_spinBox.setMinimum(0)

        # Y Label
        QLabel_Y = QLabel('Y pos:', self.update_widget_geometry_box)
        QLabel_Y.setGeometry(5, 50, 100, 40)
        # Y Spinbox
        self.Y_pos_update_spinBox = QSpinBox(self.update_widget_geometry_box)
        self.Y_pos_update_spinBox.setGeometry(70, 60, 40, 20)
        self.Y_pos_update_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.Y_pos_update_spinBox.setMaximum(4000)
        self.Y_pos_update_spinBox.setMinimum(0)

        # Width Label
        QLabel_width = QLabel('Width:', self.update_widget_geometry_box)
        QLabel_width.setGeometry(5, 80, 100, 40)
        # Width Spinbox
        self.width_update_spinBox = QSpinBox(self.update_widget_geometry_box)
        self.width_update_spinBox.setGeometry(70, 90, 40, 20)
        self.width_update_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.width_update_spinBox.setMaximum(4000)
        self.width_update_spinBox.setMinimum(0)

        # Height Label
        QLabel_height = QLabel('Height:', self.update_widget_geometry_box)
        QLabel_height.setGeometry(5, 110, 100, 40)
        # Width Spinbox
        self.height_update_spinBox = QSpinBox(self.update_widget_geometry_box)
        self.height_update_spinBox.setGeometry(70, 120, 40, 20)
        self.height_update_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
        self.height_update_spinBox.setMaximum(4000)
        self.height_update_spinBox.setMinimum(0)
        ################################################################################################################

        # ScrollArea widget update 'Widget Parameters'
        ################################################################################################################
        self.chosen_widget_update_parameters_box = QGroupBox()
        self.chosen_widget_update_parameters_box.setFixedWidth(self.widget_parameter_bar_width - 15)
        self.chosen_widget_update_parameters_box.setFixedHeight(190)
        self.chosen_widget_update_parameters_box.setTitle('Chosen Widget Parameters')
        self.chosen_widget_update_parameters_box.setStyleSheet("background-color: lightblue;")

        self.chosen_widget_update_parameters_area = QScrollArea(self.widget_parameter_box)
        self.chosen_widget_update_parameters_area.setWidget(self.chosen_widget_update_parameters_box)
        self.chosen_widget_update_parameters_area.setWidgetResizable(True)
        self.chosen_widget_update_parameters_area.setGeometry(0, 840, self.widget_parameter_bar_width, 192)

        # Edit Widget button
        self.edit_button_button = QPushButton(self.widget_parameter_box)
        self.edit_button_button.setText('Edit Widget')
        font = QFont("Arial", 10)
        self.edit_button_button.setFont(font)
        self.edit_button_button.setStyleSheet("background-color: white; padding: 0px;")
        self.edit_button_button.setGeometry(60, 1040, 120, 35)
        self.edit_button_button.clicked.connect(self.add_widget_to_window)
        ################################################################################################################

    # pasek widgetów
    def widgets_bar(self):
        self.widgets_box = QGroupBox()
        self.widgets_box.setFixedWidth(self.widgets_bar_width - 15)
        self.widgets_box.setFixedHeight(self.window_height + 500)
        self.widgets_box.setStyleSheet("background-color: lightblue;")
        self.widgets_box.setFlat(True)

        # stworzenie Scroll Area
        self.widgets_scroll_area = QScrollArea(self)
        self.widgets_scroll_area.setWidget(self.widgets_box)
        self.widgets_scroll_area.setWidgetResizable(True)
        self.widgets_scroll_area.setGeometry(int(self.tree_view_width + self.root_space_width + self.widget_parameter_bar_width), self.upper_limit, self.widgets_bar_width, self.window_height)
        self.widgets_scroll_area.setObjectName('widgets_area')
        # self.widgets_scroll_area.setStyleSheet("background-color: lightblue;")

        # QLabel 'Select window'
        self.label_select_window = QLabel(self.widgets_box)
        self.label_select_window.setText('Select Window:')
        font = QFont("Arial", 10)
        self.label_select_window.setFont(font)
        self.label_select_window.setGeometry(5, 10, 120, 35)

        # stworzenie window name comboBox
        self.window_name_comboBox = QComboBox(self.widgets_box)
        self.window_name_comboBox.setGeometry(110, 10, 80, 35)
        font = QFont("Arial", 8)
        self.window_name_comboBox.setFont(font)
        self.window_name_comboBox.setStyleSheet("background-color: white;")
        self.window_name_comboBox.setObjectName('window_name_comboBox')
        self.window_name_comboBox.setFont(font)

        # ScrollArea 'Display Widgets'
        ################################################################################################################
        self.disp_widgets_box = QGroupBox()
        self.disp_widgets_box.setFixedWidth(self.widgets_bar_width - 15)
        self.disp_widgets_box.setFixedHeight(245)
        self.disp_widgets_box.setTitle('Display Widgets')

        self.disp_widgets_area = QScrollArea(self.widgets_box)
        self.disp_widgets_area.setWidget(self.disp_widgets_box)
        self.disp_widgets_area.setWidgetResizable(True)
        self.disp_widgets_area.setGeometry(0, 50, self.widgets_bar_width, 247)

        # Qlabel icon
        QLabel_icon = QLabel(self.disp_widgets_box)
        QLabel_icon.setScaledContents(True)
        QLabel_icon.setGeometry(5, 30, 20, 20)
        QLabel_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/Label.png")))
        # Qlabel text
        QLabel_text = QLabel('Label', self.disp_widgets_box)
        QLabel_text.setGeometry(40, 20, 120, 40)
        QLabel_text.setFont(font)
        # Qlabel checkbox
        self.QLabel_checkbox = QCheckBox(self.disp_widgets_box)
        self.QLabel_checkbox.setGeometry(150, 30, 30, 20)

        # Progressbar icon
        QProgressBar_icon = QLabel(self.disp_widgets_box)
        QProgressBar_icon.setScaledContents(True)
        QProgressBar_icon.setGeometry(5, 60, 20, 20)
        QProgressBar_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/progressbar.png")))
        # Progressbar text
        QProgressbar_text = QLabel('ProgressBar', self.disp_widgets_box)
        QProgressbar_text.setGeometry(40, 50, 120, 40)
        QProgressbar_text.setFont(font)
        # Progressbar checkbox
        self.Progressbar_checkbox = QCheckBox(self.disp_widgets_box)
        self.Progressbar_checkbox.setGeometry(150, 60, 30, 20)

        # Calendar icon
        Calendar_icon = QLabel(self.disp_widgets_box)
        Calendar_icon.setScaledContents(True)
        Calendar_icon.setGeometry(5, 90, 20, 20)
        Calendar_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/calendar.png")))
        # Progressbar text
        Calendar_text = QLabel('Calendar Widget', self.disp_widgets_box)
        Calendar_text.setGeometry(40, 80, 120, 40)
        Calendar_text.setFont(font)
        # Progressbar checkbox
        self.Calendar_checkbox = QCheckBox(self.disp_widgets_box)
        self.Calendar_checkbox.setGeometry(150, 90, 30, 20)

        # Horizontal_line icon
        Horizontal_line_icon = QLabel(self.disp_widgets_box)
        Horizontal_line_icon.setScaledContents(True)
        Horizontal_line_icon.setGeometry(5, 120, 20, 20)
        Horizontal_line_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/horizontal_line.png")))
        # Horizontal_line text
        Horizontal_line_text = QLabel('Horizontal Line', self.disp_widgets_box)
        Horizontal_line_text.setGeometry(40, 110, 120, 40)
        Horizontal_line_text.setFont(font)
        # Horizontal_line checkbox
        self.Horizontal_line_checkbox = QCheckBox(self.disp_widgets_box)
        self.Horizontal_line_checkbox.setGeometry(150, 120, 30, 20)

        # Vertical_line icon
        Vertical_line_icon = QLabel(self.disp_widgets_box)
        Vertical_line_icon.setScaledContents(True)
        Vertical_line_icon.setGeometry(5, 150, 20, 20)
        Vertical_line_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/vertical_line.png")))
        # Vertical_line text
        Vertical_line_text = QLabel('Vertical Line', self.disp_widgets_box)
        Vertical_line_text.setGeometry(40, 140, 120, 40)
        Vertical_line_text.setFont(font)
        # Vertical_line checkbox
        self.Vertical_line_checkbox = QCheckBox(self.disp_widgets_box)
        self.Vertical_line_checkbox.setGeometry(150, 150, 30, 20)

        # Cirlce icon
        Cirlce_icon = QLabel(self.disp_widgets_box)
        Cirlce_icon.setScaledContents(True)
        Cirlce_icon.setGeometry(5, 180, 20, 20)
        Cirlce_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/circle.png")))
        # Cirlce text
        Cirlce_text = QLabel('Circle', self.disp_widgets_box)
        Cirlce_text.setGeometry(40, 170, 120, 40)
        Cirlce_text.setFont(font)
        # Cirlce checkbox
        self.Cirlce_checkbox = QCheckBox(self.disp_widgets_box)
        self.Cirlce_checkbox.setGeometry(150, 180, 30, 20)

        # Rectangle icon
        Rectangle_icon = QLabel(self.disp_widgets_box)
        Rectangle_icon.setScaledContents(True)
        Rectangle_icon.setGeometry(5, 210, 20, 20)
        Rectangle_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/rectangle.png")))
        # Rectangle text
        Rectangle_text = QLabel('Rectangle', self.disp_widgets_box)
        Rectangle_text.setGeometry(40, 200, 120, 40)
        Rectangle_text.setFont(font)
        # Rectangle checkbox
        self.Rectangle_checkbox = QCheckBox(self.disp_widgets_box)
        self.Rectangle_checkbox.setGeometry(150, 210, 30, 20)
        ################################################################################################################

        # ScrollArea 'Input Widgets'
        ################################################################################################################
        self.input_widgets_box = QGroupBox()
        self.input_widgets_box.setFixedWidth(self.widgets_bar_width - 15)
        self.input_widgets_box.setFixedHeight(245)
        self.input_widgets_box.setTitle('Input Widgets')

        self.input_widgets_area = QScrollArea(self.widgets_box)
        self.input_widgets_area.setWidget(self.input_widgets_box)
        self.input_widgets_area.setWidgetResizable(True)
        self.input_widgets_area.setGeometry(0, 300, self.widgets_bar_width, 247)

        # QComboBox icon
        QComboBox_icon = QLabel(self.input_widgets_box)
        QComboBox_icon.setScaledContents(True)
        QComboBox_icon.setGeometry(5, 30, 20, 20)
        QComboBox_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/comboBox.png")))
        # Qlabel text
        QComboBox_text = QLabel('ComboBox', self.input_widgets_box)
        QComboBox_text.setGeometry(40, 20, 120, 40)
        QComboBox_text.setFont(font)
        # Qlabel checkbox
        self.QComboBox_checkbox = QCheckBox(self.input_widgets_box)
        self.QComboBox_checkbox.setGeometry(150, 30, 30, 20)

        # QLineEdit icon
        QLineEdit_icon = QLabel(self.input_widgets_box)
        QLineEdit_icon.setScaledContents(True)
        QLineEdit_icon.setGeometry(5, 60, 20, 20)
        QLineEdit_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/LineEdit.png")))
        # QLineEdit text
        QLineEdit_text = QLabel('LineEdit', self.input_widgets_box)
        QLineEdit_text.setGeometry(40, 50, 120, 40)
        QLineEdit_text.setFont(font)
        # QLineEdit checkbox
        self.QLineEdit_checkbox = QCheckBox(self.input_widgets_box)
        self.QLineEdit_checkbox.setGeometry(150, 60, 30, 20)

        # QSpinBox icon
        QSpinBox_icon = QLabel(self.input_widgets_box)
        QSpinBox_icon.setScaledContents(True)
        QSpinBox_icon.setGeometry(5, 90, 20, 20)
        QSpinBox_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/spinBox.png")))
        # QSpinBox text
        QSpinBox_text = QLabel('SpinBox', self.input_widgets_box)
        QSpinBox_text.setGeometry(40, 80, 120, 40)
        QSpinBox_text.setFont(font)
        # QSpinBox checkbox
        self.QSpinBox_checkbox = QCheckBox(self.input_widgets_box)
        self.QSpinBox_checkbox.setGeometry(150, 90, 30, 20)

        # QDoubleSpinBox icon
        QDoubleSpinBox_icon = QLabel(self.input_widgets_box)
        QDoubleSpinBox_icon.setScaledContents(True)
        QDoubleSpinBox_icon.setGeometry(5, 120, 20, 20)
        QDoubleSpinBox_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/DoubleSpinBox.png")))
        # QDoubleSpinBox text
        QDoubleSpinBox_text = QLabel('DoubleSpinBox', self.input_widgets_box)
        QDoubleSpinBox_text.setGeometry(40, 110, 120, 40)
        QDoubleSpinBox_text.setFont(font)
        # QDoubleSpinBox checkbox
        self.QDoubleSpinBox_checkbox = QCheckBox(self.input_widgets_box)
        self.QDoubleSpinBox_checkbox.setGeometry(150, 120, 30, 20)

        # QDateEdit icon
        QDateEdit_icon = QLabel(self.input_widgets_box)
        QDateEdit_icon.setScaledContents(True)
        QDateEdit_icon.setGeometry(5, 150, 20, 20)
        QDateEdit_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/DateEdit.png")))
        # QDateEdit text
        QDateEdit_text = QLabel('DateEdit', self.input_widgets_box)
        QDateEdit_text.setGeometry(40, 140, 120, 40)
        QDateEdit_text.setFont(font)
        # QDateEdit checkbox
        self.QDateEdit_checkbox = QCheckBox(self.input_widgets_box)
        self.QDateEdit_checkbox.setGeometry(150, 150, 30, 20)

        # QHorizontalSilder icon
        QHorizontalSilder_icon = QLabel(self.input_widgets_box)
        QHorizontalSilder_icon.setScaledContents(True)
        QHorizontalSilder_icon.setGeometry(5, 180, 20, 20)
        QHorizontalSilder_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/Horizontal_slider.png")))
        # QHorizontalSilder text
        QHorizontalSlider_text = QLabel('Horizontal Slider', self.input_widgets_box)
        QHorizontalSlider_text.setGeometry(40, 170, 120, 40)
        QHorizontalSlider_text.setFont(font)
        # QHorizontalSilder checkbox
        self.QHorizontalSlider_checkbox = QCheckBox(self.input_widgets_box)
        self.QHorizontalSlider_checkbox.setGeometry(150, 180, 30, 20)

        # QVerticalSilder icon
        QVerticalSilder_icon = QLabel(self.input_widgets_box)
        QVerticalSilder_icon.setScaledContents(True)
        QVerticalSilder_icon.setGeometry(5, 210, 20, 20)
        QVerticalSilder_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/Vertical_slider.png")))
        # QVerticalSilder text
        QVerticalSilder_text = QLabel('Vertical Slider', self.input_widgets_box)
        QVerticalSilder_text.setGeometry(40, 200, 120, 40)
        QVerticalSilder_text.setFont(font)
        # QVerticalSilder checkbox
        self.QVerticalSilder_checkbox = QCheckBox(self.input_widgets_box)
        self.QVerticalSilder_checkbox.setGeometry(150, 210, 30, 20)
        ################################################################################################################

        # ScrollArea 'Buttons'
        ################################################################################################################
        self.buttons_groupBox = QGroupBox()
        self.buttons_groupBox.setFixedWidth(self.widgets_bar_width - 15)
        self.buttons_groupBox.setFixedHeight(100)
        self.buttons_groupBox.setTitle('Buttons')

        self.buttons_area = QScrollArea(self.widgets_box)
        self.buttons_area.setWidget(self.buttons_groupBox)
        self.buttons_area.setWidgetResizable(True)
        self.buttons_area.setGeometry(0, 550, self.widgets_bar_width, 102)

        # QPushButton icon
        QPushButton_icon = QLabel(self.buttons_groupBox)
        QPushButton_icon.setScaledContents(True)
        QPushButton_icon.setGeometry(5, 30, 20, 20)
        QPushButton_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/Button.png")))
        # QPushButton text
        QPushButton_text = QLabel('PushButton', self.buttons_groupBox)
        QPushButton_text.setGeometry(40, 20, 120, 40)
        QPushButton_text.setFont(font)
        # QPushButton checkbox
        self.QPushButton_checkbox = QCheckBox(self.buttons_groupBox)
        self.QPushButton_checkbox.setGeometry(150, 30, 30, 20)

        # QCheckBox icon
        QCheckBox_icon = QLabel(self.buttons_groupBox)
        QCheckBox_icon.setScaledContents(True)
        QCheckBox_icon.setGeometry(5, 60, 20, 20)
        QCheckBox_icon.setPixmap(QPixmap(os.path.join(BASEDIR, "ikonki/CheckBox.png")))
        # QCheckBox text
        QCheckBox_text = QLabel('CheckBox', self.buttons_groupBox)
        QCheckBox_text.setGeometry(40, 50, 120, 40)
        QCheckBox_text.setFont(font)
        # QCheckBox checkbox
        self.QCheckBox_checkbox = QCheckBox(self.buttons_groupBox)
        self.QCheckBox_checkbox.setGeometry(150, 60, 30, 20)
        ################################################################################################################

        # stworzenie grupy checkboxów i ustawienie żeby tylko jeden mógł być zaznaczony
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        # dodanie checkboxy do grupy
        self.button_group.addButton(self.QLabel_checkbox)
        self.button_group.addButton(self.Progressbar_checkbox)
        self.button_group.addButton(self.Calendar_checkbox)
        self.button_group.addButton(self.Horizontal_line_checkbox)
        self.button_group.addButton(self.Vertical_line_checkbox)
        self.button_group.addButton(self.Cirlce_checkbox)
        self.button_group.addButton(self.Rectangle_checkbox)
        self.button_group.addButton(self.QComboBox_checkbox)
        self.button_group.addButton(self.QLineEdit_checkbox)
        self.button_group.addButton(self.QSpinBox_checkbox)
        self.button_group.addButton(self.QDoubleSpinBox_checkbox)
        self.button_group.addButton(self.QDateEdit_checkbox)
        self.button_group.addButton(self.QHorizontalSlider_checkbox)
        self.button_group.addButton(self.QVerticalSilder_checkbox)
        self.button_group.addButton(self.QPushButton_checkbox)
        self.button_group.addButton(self.QCheckBox_checkbox)

        # zmiana checkboxa wywołuje metodę 'on_checkbox_toggled'
        self.button_group.buttonToggled.connect(self.on_checkbox_toggled)

    def on_checkbox_toggled(self, button, checked):
        # wyczyszczenie groupboxa
        for child in self.chosen_widget_parameters_box.findChildren(QWidget):  # Znajdź wszystkie widgety wewnątrz
            child.setParent(None)  # Odłącz od rodzica, Qt sam go usunie
        if checked:
            match button:
                case self.QLabel_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Text Label
                    QLabel_text = QLabel('Text:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_text.setFont(font)
                    QLabel_text.setGeometry(5, 50, 100, 35)
                    QLabel_text.show()
                    # Text lineEdit
                    self.text_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.text_lineEdit.setGeometry(100, 57, 110, 20)
                    self.text_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.text_lineEdit.show()


                    # Font Label
                    QLabel_font_family = QLabel('Family Font:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_font_family.setFont(font)
                    QLabel_font_family.setGeometry(5, 80, 100, 35)
                    QLabel_font_family.show()
                    # font family ComboBox
                    self.font_family_comboBox = QFontComboBox(self.chosen_widget_parameters_box)
                    self.font_family_comboBox.setGeometry(100, 87, 110, 20)
                    self.font_family_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.font_family_comboBox.setEditable(False)
                    self.font_family_comboBox.show()

                    # Font size
                    QLabel_font_size = QLabel('Family Size:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_font_size.setFont(font)
                    QLabel_font_size.setGeometry(5, 110, 100, 35)
                    QLabel_font_size.show()
                    # font Size SpinBox
                    self.font_size_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.font_size_SpinBox.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.font_size_SpinBox.setFont(font)
                    self.font_size_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.font_size_SpinBox.setMinimum(1)
                    self.font_size_SpinBox.setMaximum(100)
                    self.font_size_SpinBox.show()

                    # Bold
                    QLabel_bold = QLabel('Bold:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_bold.setFont(font)
                    QLabel_bold.setGeometry(5, 140, 100, 35)
                    QLabel_bold.show()
                    # Bold Checkbox
                    self.bold_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.bold_checkBox.setGeometry(102, 147, 110, 20)
                    self.bold_checkBox.setFont(font)
                    self.bold_checkBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.Progressbar_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Min value Label
                    QLabel_min_value = QLabel('Min Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_value.setFont(font)
                    QLabel_min_value.setGeometry(5, 50, 100, 35)
                    QLabel_min_value.show()
                    # Min value SpinBox
                    self.min_value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.min_value_SpinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.min_value_SpinBox.setFont(font)
                    self.min_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_value_SpinBox.setMinimum(-99999)
                    self.min_value_SpinBox.setMaximum(99999)
                    self.min_value_SpinBox.setValue(0)
                    self.min_value_SpinBox.show()

                    # Max value Label
                    QLabel_max_value = QLabel('Max Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_value.setFont(font)
                    QLabel_max_value.setGeometry(5, 80, 100, 35)
                    QLabel_max_value.show()
                    # Max value SpinBox
                    self.max_value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.max_value_SpinBox.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 9)
                    self.max_value_SpinBox.setFont(font)
                    self.max_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_value_SpinBox.setMinimum(-99999)
                    self.max_value_SpinBox.setMaximum(99999)
                    self.max_value_SpinBox.setValue(100)
                    self.max_value_SpinBox.show()

                    # Value Label
                    QLabel_value = QLabel('Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_value.setFont(font)
                    QLabel_value.setGeometry(5, 110, 100, 35)
                    QLabel_value.show()
                    # Value SpinBox
                    self.value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.value_SpinBox.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.value_SpinBox.setFont(font)
                    self.value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.value_SpinBox.show()

                    # Połączenie sygnałów zmiany wartości min/max SpinBoxa
                    self.min_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))
                    self.max_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))

                    # Ustawienie domyślnego zakres
                    self.update_value_spinbox_range(type='add')

                    # Orientation Label
                    QLabel_orientation = QLabel('Orientation:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_orientation.setFont(font)
                    QLabel_orientation.setGeometry(5, 140, 100, 35)
                    QLabel_orientation.show()
                    # Orientation ComboBox
                    self.orientation_comboBox = QComboBox(self.chosen_widget_parameters_box)
                    self.orientation_comboBox.setGeometry(100, 147, 110, 20)
                    font = QFont('Arial', 8)
                    self.orientation_comboBox.setFont(font)
                    self.orientation_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.orientation_comboBox.addItem('Horizontal')
                    self.orientation_comboBox.addItem('Vertical')
                    self.orientation_comboBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.Calendar_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Min date Label
                    QLabel_min_date = QLabel('Min Date:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_date.setFont(font)
                    QLabel_min_date.setGeometry(5, 50, 100, 35)
                    QLabel_min_date.show()
                    # Min value DateEdit
                    self.min_date_dateEdit = QDateEdit(self.chosen_widget_parameters_box)
                    self.min_date_dateEdit.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 8)
                    self.min_date_dateEdit.setFont(font)
                    self.min_date_dateEdit.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_date_dateEdit.setMinimumDate(QDate(1000, 1, 1))
                    self.min_date_dateEdit.setMaximumDate(QDate(9999, 12, 31))
                    self.min_date_dateEdit.setDate(QDate(1752, 2, 14))
                    self.min_date_dateEdit.setCalendarPopup(True)
                    self.min_date_dateEdit.show()

                    # Max date Label
                    QLabel_max_date = QLabel('Max Date:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_date.setFont(font)
                    QLabel_max_date.setGeometry(5, 80, 100, 35)
                    QLabel_max_date.show()
                    # Min value DateEdit
                    self.max_date_dateEdit = QDateEdit(self.chosen_widget_parameters_box)
                    self.max_date_dateEdit.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 8)
                    self.max_date_dateEdit.setFont(font)
                    self.max_date_dateEdit.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_date_dateEdit.setMinimumDate(QDate(1000, 1, 1))
                    self.max_date_dateEdit.setMaximumDate(QDate(9999, 12, 31))
                    self.max_date_dateEdit.setDate(QDate(9999, 12, 31))
                    self.max_date_dateEdit.setCalendarPopup(True)
                    self.max_date_dateEdit.show()

                    # Set date Label
                    QLabel_set_date = QLabel('Set Date:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_set_date.setFont(font)
                    QLabel_set_date.setGeometry(5, 110, 100, 35)
                    QLabel_set_date.show()
                    # Set date DateEdit
                    self.set_date_dateEdit = QDateEdit(self.chosen_widget_parameters_box)
                    self.set_date_dateEdit.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 8)
                    self.set_date_dateEdit.setFont(font)
                    self.set_date_dateEdit.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.set_date_dateEdit.setMinimumDate(QDate(1000, 1, 1))
                    self.set_date_dateEdit.setMaximumDate(QDate(9999, 12, 31))
                    self.set_date_dateEdit.setDate(QDate(date.today().year, date.today().month, date.today().day))
                    self.set_date_dateEdit.setCalendarPopup(True)
                    self.set_date_dateEdit.show()

                    self.min_date_dateEdit.dateChanged.connect(lambda: self.update_date_range(type='add'))
                    self.max_date_dateEdit.dateChanged.connect(lambda: self.update_date_range(type='add'))

                    # Grid Visible Label
                    QLabel_grid = QLabel('Grid Visible:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_grid.setFont(font)
                    QLabel_grid.setGeometry(5, 140, 100, 35)
                    QLabel_grid.show()
                    # Grid Visible Checkbox
                    self.grid_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.grid_checkBox.setGeometry(102, 147, 110, 20)
                    self.grid_checkBox.setFont(font)
                    self.grid_checkBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.Horizontal_line_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Width Label
                    QLabel_width = QLabel('Line Width:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_width.setFont(font)
                    QLabel_width.setGeometry(5, 50, 100, 35)
                    QLabel_width.show()
                    # Width SpinBox
                    self.widthLine_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.widthLine_SpinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.widthLine_SpinBox.setFont(font)
                    self.widthLine_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.widthLine_SpinBox.setMinimum(1)
                    self.widthLine_SpinBox.setMaximum(99999)
                    self.widthLine_SpinBox.show()

                    # Frame Shadow Label
                    QLabel_frame = QLabel('Frame:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_frame.setFont(font)
                    QLabel_frame.setGeometry(5, 80, 100, 35)
                    QLabel_frame.show()
                    # Frame Shadow ComboBox
                    self.frame_comboBox = QComboBox(self.chosen_widget_parameters_box)
                    self.frame_comboBox.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 8)
                    self.frame_comboBox.setFont(font)
                    self.frame_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.frame_comboBox.addItem('Plain')
                    self.frame_comboBox.addItem('Raised')
                    self.frame_comboBox.addItem('Sunken')
                    self.frame_comboBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.Vertical_line_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Width Label
                    QLabel_width = QLabel('Line Width:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_width.setFont(font)
                    QLabel_width.setGeometry(5, 50, 100, 35)
                    QLabel_width.show()
                    # Width SpinBox
                    self.widthLine_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.widthLine_SpinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.widthLine_SpinBox.setFont(font)
                    self.widthLine_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.widthLine_SpinBox.setMinimum(1)
                    self.widthLine_SpinBox.setMaximum(99999)
                    self.widthLine_SpinBox.show()

                    # Frame Shadow Label
                    QLabel_frame = QLabel('Frame:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_frame.setFont(font)
                    QLabel_frame.setGeometry(5, 80, 100, 35)
                    QLabel_frame.show()
                    # Frame Shadow ComboBox
                    self.frame_comboBox = QComboBox(self.chosen_widget_parameters_box)
                    self.frame_comboBox.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 8)
                    self.frame_comboBox.setFont(font)
                    self.frame_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.frame_comboBox.addItem('Plain')
                    self.frame_comboBox.addItem('Raised')
                    self.frame_comboBox.addItem('Sunken')
                    self.frame_comboBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.QComboBox_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # MaxVisibleItems Label
                    QLabel_max_visible_items = QLabel('maxVisItems:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_visible_items.setFont(font)
                    QLabel_max_visible_items.setGeometry(5, 50, 100, 35)
                    QLabel_max_visible_items.show()
                    # MaxVisibleItems SpinBox
                    self.max_visible_items_spinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.max_visible_items_spinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.max_visible_items_spinBox.setFont(font)
                    self.max_visible_items_spinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_visible_items_spinBox.setMinimum(0)
                    self.max_visible_items_spinBox.setMaximum(99999)
                    self.max_visible_items_spinBox.setValue(10)
                    self.max_visible_items_spinBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.QLineEdit_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Text Label
                    QLabel_text = QLabel('Text:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_text.setFont(font)
                    QLabel_text.setGeometry(5, 50, 100, 35)
                    QLabel_text.show()
                    # Object Name lineEdit
                    self.text_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.text_lineEdit.setGeometry(100, 57, 110, 20)
                    self.text_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.text_lineEdit.show()

                    # Font Label
                    QLabel_font_family = QLabel('Family Font:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_font_family.setFont(font)
                    QLabel_font_family.setGeometry(5, 80, 100, 35)
                    QLabel_font_family.show()
                    # font family ComboBox
                    self.font_family_comboBox = QFontComboBox(self.chosen_widget_parameters_box)
                    self.font_family_comboBox.setGeometry(100, 87, 110, 20)
                    self.font_family_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.font_family_comboBox.setEditable(False)
                    self.font_family_comboBox.show()

                    # Font size
                    QLabel_font_size = QLabel('Family Size:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_font_size.setFont(font)
                    QLabel_font_size.setGeometry(5, 110, 100, 35)
                    QLabel_font_size.show()
                    # font Size SpinBox
                    self.font_size_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.font_size_SpinBox.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.font_size_SpinBox.setFont(font)
                    self.font_size_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.font_size_SpinBox.setMinimum(1)
                    self.font_size_SpinBox.setMaximum(100)
                    self.font_size_SpinBox.show()

                    # Read Only
                    QLabel_read_only = QLabel('Read Only:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_read_only.setFont(font)
                    QLabel_read_only.setGeometry(5, 140, 100, 35)
                    QLabel_read_only.show()
                    # Bold Checkbox
                    self.read_only_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.read_only_checkBox.setGeometry(102, 147, 110, 20)
                    self.read_only_checkBox.setFont(font)
                    self.read_only_checkBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.QSpinBox_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # min value
                    QLabel_min_value = QLabel('Min Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_value.setFont(font)
                    QLabel_min_value.setGeometry(5, 50, 100, 35)
                    QLabel_min_value.show()
                    # font min value SpinBox
                    self.min_value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.min_value_SpinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.min_value_SpinBox.setFont(font)
                    self.min_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_value_SpinBox.setMinimum(-999999999)
                    self.min_value_SpinBox.setMaximum(999999999)
                    self.min_value_SpinBox.setValue(1)
                    self.min_value_SpinBox.show()

                    # max value
                    QLabel_max_value = QLabel('Max Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_value.setFont(font)
                    QLabel_max_value.setGeometry(5, 80, 100, 35)
                    QLabel_max_value.show()
                    # max value SpinBox
                    self.max_value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.max_value_SpinBox.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 9)
                    self.max_value_SpinBox.setFont(font)
                    self.max_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_value_SpinBox.setMinimum(-999999999)
                    self.max_value_SpinBox.setMaximum(999999999)
                    self.max_value_SpinBox.setValue(999)
                    self.max_value_SpinBox.show()

                    # value
                    QLabel_value = QLabel('Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_value.setFont(font)
                    QLabel_value.setGeometry(5, 110, 100, 35)
                    QLabel_value.show()
                    # value SpinBox
                    self.value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.value_SpinBox.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.value_SpinBox.setFont(font)
                    self.value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.value_SpinBox.setMinimum(-999999999)
                    self.value_SpinBox.setMaximum(999999999)
                    self.value_SpinBox.show()

                    # Połączenie sygnałów zmiany wartości min/max SpinBoxa
                    self.min_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))
                    self.max_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))

                    # Ustawienie domyślnego zakres
                    self.update_value_spinbox_range(type='add')

                    # singleStep
                    QLabel_singleStep = QLabel('Single Step:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_singleStep.setFont(font)
                    QLabel_singleStep.setGeometry(5, 140, 100, 35)
                    QLabel_singleStep.show()
                    # singleStep SpinBox
                    self.singleStep_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.singleStep_SpinBox.setGeometry(100, 147, 110, 20)
                    font = QFont('Arial', 9)
                    self.singleStep_SpinBox.setFont(font)
                    self.singleStep_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.singleStep_SpinBox.setMinimum(1)
                    self.singleStep_SpinBox.setMaximum(999999999)
                    self.singleStep_SpinBox.show()

                    # Prefix Label
                    QLabel_prfix = QLabel('Prefix:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_prfix.setFont(font)
                    QLabel_prfix.setGeometry(5, 170, 100, 35)
                    QLabel_prfix.show()
                    # Prefix lineEdit
                    self.prefix_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.prefix_lineEdit.setGeometry(100, 177, 110, 20)
                    self.prefix_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.prefix_lineEdit.show()

                    # Suffix Label
                    QLabel_suffix = QLabel('Suffix:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_suffix.setFont(font)
                    QLabel_suffix.setGeometry(5, 200, 100, 35)
                    QLabel_suffix.show()
                    # Prefix lineEdit
                    self.suffix_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.suffix_lineEdit.setGeometry(100, 207, 110, 20)
                    self.suffix_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.suffix_lineEdit.show()

                    self.chosen_widget_parameters_box.setFixedHeight(250)

                case self.QDoubleSpinBox_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # min value
                    QLabel_min_value = QLabel('Min Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_value.setFont(font)
                    QLabel_min_value.setGeometry(5, 50, 100, 35)
                    QLabel_min_value.show()
                    # font min value SpinBox
                    self.min_value_SpinBox = QDoubleSpinBox(self.chosen_widget_parameters_box)
                    self.min_value_SpinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.min_value_SpinBox.setFont(font)
                    self.min_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_value_SpinBox.setMinimum(-999999999)
                    self.min_value_SpinBox.setMaximum(999999999)
                    self.min_value_SpinBox.setSingleStep(0.1)
                    self.min_value_SpinBox.setDecimals(5)
                    self.min_value_SpinBox.show()

                    # max value
                    QLabel_max_value = QLabel('Max Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_value.setFont(font)
                    QLabel_max_value.setGeometry(5, 80, 100, 35)
                    QLabel_max_value.show()
                    # max value SpinBox
                    self.max_value_SpinBox = QDoubleSpinBox(self.chosen_widget_parameters_box)
                    self.max_value_SpinBox.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 9)
                    self.max_value_SpinBox.setFont(font)
                    self.max_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_value_SpinBox.setMinimum(-999999999)
                    self.max_value_SpinBox.setMaximum(999999999)
                    self.max_value_SpinBox.setSingleStep(0.1)
                    self.max_value_SpinBox.setValue(99.9)
                    self.max_value_SpinBox.setDecimals(5)
                    self.max_value_SpinBox.show()

                    # value
                    QLabel_value = QLabel('Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_value.setFont(font)
                    QLabel_value.setGeometry(5, 110, 100, 35)
                    QLabel_value.show()
                    # value SpinBox
                    self.value_SpinBox = QDoubleSpinBox(self.chosen_widget_parameters_box)
                    self.value_SpinBox.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.value_SpinBox.setFont(font)
                    self.value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.value_SpinBox.setMinimum(-999999999)
                    self.value_SpinBox.setMaximum(999999999)
                    self.value_SpinBox.setSingleStep(0.1)
                    self.value_SpinBox.setDecimals(5)
                    self.value_SpinBox.show()

                    # Połączenie sygnałów zmiany wartości min/max SpinBoxa
                    self.min_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))
                    self.max_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))

                    # Ustawienie domyślnego zakres
                    self.update_value_spinbox_range(type='add')

                    # singleStep
                    QLabel_singleStep = QLabel('Single Step:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_singleStep.setFont(font)
                    QLabel_singleStep.setGeometry(5, 140, 100, 35)
                    QLabel_singleStep.show()
                    # singleStep SpinBox
                    self.singleStep_SpinBox = QDoubleSpinBox(self.chosen_widget_parameters_box)
                    self.singleStep_SpinBox.setGeometry(100, 147, 110, 20)
                    font = QFont('Arial', 9)
                    self.singleStep_SpinBox.setFont(font)
                    self.singleStep_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.singleStep_SpinBox.setMinimum(0.000001)
                    self.singleStep_SpinBox.setMaximum(999999999)
                    self.singleStep_SpinBox.setSingleStep(0.1)
                    self.singleStep_SpinBox.setDecimals(5)
                    self.singleStep_SpinBox.show()

                    # Decimal
                    QLabel_decimal = QLabel('Decimal:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_decimal.setFont(font)
                    QLabel_decimal.setGeometry(5, 170, 100, 35)
                    QLabel_decimal.show()
                    # Decimal SpinBox
                    self.decimal_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.decimal_SpinBox.setGeometry(100, 177, 110, 20)
                    font = QFont('Arial', 9)
                    self.decimal_SpinBox.setFont(font)
                    self.decimal_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.decimal_SpinBox.setMinimum(0)
                    self.decimal_SpinBox.setMaximum(5)
                    self.decimal_SpinBox.show()

                    # Prefix Label
                    QLabel_prfix = QLabel('Prefix:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_prfix.setFont(font)
                    QLabel_prfix.setGeometry(5, 200, 100, 35)
                    QLabel_prfix.show()
                    # Prefix lineEdit
                    self.prefix_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.prefix_lineEdit.setGeometry(100, 207, 110, 20)
                    self.prefix_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.prefix_lineEdit.show()

                    # Suffix Label
                    QLabel_suffix = QLabel('Suffix:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_suffix.setFont(font)
                    QLabel_suffix.setGeometry(5, 230, 100, 35)
                    QLabel_suffix.show()
                    # Prefix lineEdit
                    self.suffix_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.suffix_lineEdit.setGeometry(100, 237, 110, 20)
                    self.suffix_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.suffix_lineEdit.show()

                    self.chosen_widget_parameters_box.setFixedHeight(280)

                case self.QDateEdit_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Min date Label
                    QLabel_min_date = QLabel('Min Date:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_date.setFont(font)
                    QLabel_min_date.setGeometry(5, 50, 100, 35)
                    QLabel_min_date.show()
                    # Min value DateEdit
                    self.min_date_dateEdit = QDateEdit(self.chosen_widget_parameters_box)
                    self.min_date_dateEdit.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 8)
                    self.min_date_dateEdit.setFont(font)
                    self.min_date_dateEdit.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_date_dateEdit.setMinimumDate(QDate(1000, 1, 1))
                    self.min_date_dateEdit.setMaximumDate(QDate(9999, 12, 31))
                    self.min_date_dateEdit.setDate(QDate(1752, 2, 14))
                    self.min_date_dateEdit.setCalendarPopup(True)
                    self.min_date_dateEdit.show()

                    # Max date Label
                    QLabel_max_date = QLabel('Max Date:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_date.setFont(font)
                    QLabel_max_date.setGeometry(5, 80, 100, 35)
                    QLabel_max_date.show()
                    # Min value DateEdit
                    self.max_date_dateEdit = QDateEdit(self.chosen_widget_parameters_box)
                    self.max_date_dateEdit.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 8)
                    self.max_date_dateEdit.setFont(font)
                    self.max_date_dateEdit.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_date_dateEdit.setMinimumDate(QDate(1000, 1, 1))
                    self.max_date_dateEdit.setMaximumDate(QDate(9999, 12, 31))
                    self.max_date_dateEdit.setDate(QDate(9999, 12, 31))
                    self.max_date_dateEdit.setCalendarPopup(True)
                    self.max_date_dateEdit.show()

                    # Set date Label
                    QLabel_set_date = QLabel('Set Date:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_set_date.setFont(font)
                    QLabel_set_date.setGeometry(5, 110, 100, 35)
                    QLabel_set_date.show()
                    # Set date DateEdit
                    self.set_date_dateEdit = QDateEdit(self.chosen_widget_parameters_box)
                    self.set_date_dateEdit.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 8)
                    self.set_date_dateEdit.setFont(font)
                    self.set_date_dateEdit.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.set_date_dateEdit.setMinimumDate(QDate(1000, 1, 1))
                    self.set_date_dateEdit.setMaximumDate(QDate(9999, 12, 31))
                    self.set_date_dateEdit.setDate(QDate(date.today().year, date.today().month, date.today().day))
                    self.set_date_dateEdit.setCalendarPopup(True)
                    self.set_date_dateEdit.show()

                    self.min_date_dateEdit.dateChanged.connect(lambda: self.update_date_range(type='add'))
                    self.max_date_dateEdit.dateChanged.connect(lambda: self.update_date_range(type='add'))

                    # Calendar Popup
                    QLabel_calendar_popup = QLabel('CalPopup :', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_calendar_popup.setFont(font)
                    QLabel_calendar_popup.setGeometry(5, 140, 100, 35)
                    QLabel_calendar_popup.show()
                    # Calendar Popup
                    self.calendar_popup_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.calendar_popup_checkBox.setGeometry(102, 147, 110, 20)
                    self.calendar_popup_checkBox.setFont(font)
                    self.calendar_popup_checkBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.QHorizontalSlider_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # min value
                    QLabel_min_value = QLabel('Min Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_value.setFont(font)
                    QLabel_min_value.setGeometry(5, 50, 100, 35)
                    QLabel_min_value.show()
                    # font min value SpinBox
                    self.min_value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.min_value_SpinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.min_value_SpinBox.setFont(font)
                    self.min_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_value_SpinBox.setMinimum(-999999999)
                    self.min_value_SpinBox.setMaximum(999999999)
                    self.min_value_SpinBox.setValue(1)
                    self.min_value_SpinBox.show()

                    # max value
                    QLabel_max_value = QLabel('Max Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_value.setFont(font)
                    QLabel_max_value.setGeometry(5, 80, 100, 35)
                    QLabel_max_value.show()
                    # max value SpinBox
                    self.max_value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.max_value_SpinBox.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 9)
                    self.max_value_SpinBox.setFont(font)
                    self.max_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_value_SpinBox.setMinimum(-999999999)
                    self.max_value_SpinBox.setMaximum(999999999)
                    self.max_value_SpinBox.setValue(999)
                    self.max_value_SpinBox.show()

                    # value
                    QLabel_value = QLabel('Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_value.setFont(font)
                    QLabel_value.setGeometry(5, 110, 100, 35)
                    QLabel_value.show()
                    # value SpinBox
                    self.value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.value_SpinBox.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.value_SpinBox.setFont(font)
                    self.value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.value_SpinBox.setMinimum(-999999999)
                    self.value_SpinBox.setMaximum(999999999)
                    self.value_SpinBox.show()

                    # Połączenie sygnałów zmiany wartości min/max SpinBoxa
                    self.min_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))
                    self.max_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))

                    # Ustawienie domyślnego zakres
                    self.update_value_spinbox_range(type='add')

                    # singleStep
                    QLabel_singleStep = QLabel('Single Step:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_singleStep.setFont(font)
                    QLabel_singleStep.setGeometry(5, 140, 100, 35)
                    QLabel_singleStep.show()
                    # singleStep SpinBox
                    self.singleStep_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.singleStep_SpinBox.setGeometry(100, 147, 110, 20)
                    font = QFont('Arial', 9)
                    self.singleStep_SpinBox.setFont(font)
                    self.singleStep_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.singleStep_SpinBox.setMinimum(1)
                    self.singleStep_SpinBox.setMaximum(999999999)
                    self.singleStep_SpinBox.show()

                    # PageStep
                    QLabel_pageStep = QLabel('Page Step:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_pageStep.setFont(font)
                    QLabel_pageStep.setGeometry(5, 170, 100, 35)
                    QLabel_pageStep.show()
                    # pageStep SpinBox
                    self.pageStep_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.pageStep_SpinBox.setGeometry(100, 177, 110, 20)
                    font = QFont('Arial', 9)
                    self.pageStep_SpinBox.setFont(font)
                    self.pageStep_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.pageStep_SpinBox.setMinimum(1)
                    self.pageStep_SpinBox.setMaximum(999999999)
                    self.pageStep_SpinBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(210)

                case self.QVerticalSilder_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # min value
                    QLabel_min_value = QLabel('Min Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_value.setFont(font)
                    QLabel_min_value.setGeometry(5, 50, 100, 35)
                    QLabel_min_value.show()
                    # font min value SpinBox
                    self.min_value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.min_value_SpinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.min_value_SpinBox.setFont(font)
                    self.min_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_value_SpinBox.setMinimum(-999999999)
                    self.min_value_SpinBox.setMaximum(999999999)
                    self.min_value_SpinBox.setValue(1)
                    self.min_value_SpinBox.show()

                    # max value
                    QLabel_max_value = QLabel('Max Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_value.setFont(font)
                    QLabel_max_value.setGeometry(5, 80, 100, 35)
                    QLabel_max_value.show()
                    # max value SpinBox
                    self.max_value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.max_value_SpinBox.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 9)
                    self.max_value_SpinBox.setFont(font)
                    self.max_value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_value_SpinBox.setMinimum(-999999999)
                    self.max_value_SpinBox.setMaximum(999999999)
                    self.max_value_SpinBox.setValue(999)
                    self.max_value_SpinBox.show()

                    # value
                    QLabel_value = QLabel('Value:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_value.setFont(font)
                    QLabel_value.setGeometry(5, 110, 100, 35)
                    QLabel_value.show()
                    # value SpinBox
                    self.value_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.value_SpinBox.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.value_SpinBox.setFont(font)
                    self.value_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.value_SpinBox.setMinimum(-999999999)
                    self.value_SpinBox.setMaximum(999999999)
                    self.value_SpinBox.show()

                    # Połączenie sygnałów zmiany wartości min/max SpinBoxa
                    self.min_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))
                    self.max_value_SpinBox.valueChanged.connect(lambda: self.update_value_spinbox_range(type='add'))

                    # Ustawienie domyślnego zakres
                    self.update_value_spinbox_range(type='add')

                    # singleStep
                    QLabel_singleStep = QLabel('Single Step:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_singleStep.setFont(font)
                    QLabel_singleStep.setGeometry(5, 140, 100, 35)
                    QLabel_singleStep.show()
                    # singleStep SpinBox
                    self.singleStep_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.singleStep_SpinBox.setGeometry(100, 147, 110, 20)
                    font = QFont('Arial', 9)
                    self.singleStep_SpinBox.setFont(font)
                    self.singleStep_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.singleStep_SpinBox.setMinimum(1)
                    self.singleStep_SpinBox.setMaximum(999999999)
                    self.singleStep_SpinBox.show()

                    # PageStep
                    QLabel_pageStep = QLabel('Page Step:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_pageStep.setFont(font)
                    QLabel_pageStep.setGeometry(5, 170, 100, 35)
                    QLabel_pageStep.show()
                    # pageStep SpinBox
                    self.pageStep_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.pageStep_SpinBox.setGeometry(100, 177, 110, 20)
                    font = QFont('Arial', 9)
                    self.pageStep_SpinBox.setFont(font)
                    self.pageStep_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.pageStep_SpinBox.setMinimum(1)
                    self.pageStep_SpinBox.setMaximum(999999999)
                    self.pageStep_SpinBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(210)

                case self.QPushButton_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Text Label
                    QLabel_text = QLabel('Text:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_text.setFont(font)
                    QLabel_text.setGeometry(5, 50, 100, 35)
                    QLabel_text.show()
                    # Object Name lineEdit
                    self.text_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.text_lineEdit.setGeometry(100, 57, 110, 20)
                    self.text_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.text_lineEdit.show()

                    # Checkable
                    QLabel_checkable = QLabel('Checkable:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_checkable.setFont(font)
                    QLabel_checkable.setGeometry(5, 80, 100, 35)
                    QLabel_checkable.show()
                    # Checkable checkbox
                    self.checkable_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.checkable_checkBox.setGeometry(102, 87, 110, 20)
                    self.checkable_checkBox.setFont(font)
                    self.checkable_checkBox.show()

                    # Checked
                    QLabel_checked = QLabel('Checked:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_checked.setFont(font)
                    QLabel_checked.setGeometry(5, 110, 100, 35)
                    QLabel_checked.show()
                    # Checked checkbox
                    self.checked_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.checked_checkBox.setGeometry(102, 117, 110, 20)
                    self.checked_checkBox.setFont(font)
                    self.checked_checkBox.setEnabled(False)
                    self.checked_checkBox.show()

                    self.checkable_checkBox.toggled.connect(self.checked_checkBox.setEnabled)
                    self.checkable_checkBox.toggled.connect(lambda: self.checked_checkBox.setChecked(False))

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.QCheckBox_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Text Label
                    QLabel_text = QLabel('Text:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_text.setFont(font)
                    QLabel_text.setGeometry(5, 50, 100, 35)
                    QLabel_text.show()
                    # Object Name lineEdit
                    self.text_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.text_lineEdit.setGeometry(100, 57, 110, 20)
                    self.text_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.text_lineEdit.show()

                    # Font Label
                    QLabel_font_family = QLabel('Family Font:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_font_family.setFont(font)
                    QLabel_font_family.setGeometry(5, 80, 100, 35)
                    QLabel_font_family.show()
                    # font family ComboBox
                    self.font_family_comboBox = QFontComboBox(self.chosen_widget_parameters_box)
                    self.font_family_comboBox.setGeometry(100, 87, 110, 20)
                    self.font_family_comboBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.font_family_comboBox.setEditable(False)
                    self.font_family_comboBox.show()

                    # Font size
                    QLabel_font_size = QLabel('Family Size:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_font_size.setFont(font)
                    QLabel_font_size.setGeometry(5, 110, 100, 35)
                    QLabel_font_size.show()
                    # font Size SpinBox
                    self.font_size_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.font_size_SpinBox.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.font_size_SpinBox.setFont(font)
                    self.font_size_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.font_size_SpinBox.setMinimum(1)
                    self.font_size_SpinBox.setMaximum(100)
                    self.font_size_SpinBox.show()

                    # Checkable
                    QLabel_checkable = QLabel('Checkable:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_checkable.setFont(font)
                    QLabel_checkable.setGeometry(5, 140, 100, 35)
                    QLabel_checkable.show()
                    # Checkable checkbox
                    self.checkable_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.checkable_checkBox.setGeometry(102, 147, 110, 20)
                    self.checkable_checkBox.setFont(font)
                    self.checkable_checkBox.setChecked(True)
                    self.checkable_checkBox.show()

                    # Checked
                    QLabel_checked = QLabel('Checked:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_checked.setFont(font)
                    QLabel_checked.setGeometry(5, 170, 100, 35)
                    QLabel_checked.show()
                    # Checked checkbox
                    self.checked_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.checked_checkBox.setGeometry(102, 177, 110, 20)
                    self.checked_checkBox.setFont(font)
                    self.checked_checkBox.setEnabled(True)
                    self.checked_checkBox.show()

                    self.checkable_checkBox.toggled.connect(self.checked_checkBox.setEnabled)
                    self.checkable_checkBox.toggled.connect(lambda: self.checked_checkBox.setChecked(False))

                    self.chosen_widget_parameters_box.setFixedHeight(220)

                case self.Cirlce_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Diameter
                    QLabel_diameter = QLabel('Diameter:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_diameter.setFont(font)
                    QLabel_diameter.setGeometry(5, 50, 100, 35)
                    QLabel_diameter.show()
                    # Diameter SpinBox
                    self.diameter_SpinBox = QSpinBox(self.chosen_widget_parameters_box)
                    self.diameter_SpinBox.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.diameter_SpinBox.setFont(font)
                    self.diameter_SpinBox.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.diameter_SpinBox.setMinimum(1)
                    self.diameter_SpinBox.setMaximum(999999999)
                    self.diameter_SpinBox.show()

                    # Color label
                    QLabel_diameter = QLabel('Color:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_diameter.setFont(font)
                    QLabel_diameter.setGeometry(5, 80, 100, 35)
                    QLabel_diameter.show()
                    # Color LineEdit
                    self.color_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.color_lineEdit.setGeometry(100, 87, 55, 20)
                    self.color_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.color_lineEdit.show()
                    # Color Pushbutton
                    self.color_button = QPushButton(self.chosen_widget_parameters_box)
                    self.color_button.setText('Color')
                    self.font = QFont('Arial', 12)
                    self.color_button.setFont(font)
                    self.color_button.setGeometry(160, 85, 50, 25)
                    self.color_button.setStyleSheet("background-color: white; padding: 0px;")
                    self.color_button.show()

                    # connect to choose color dialog
                    self.color_button.clicked.connect(self.choose_color)

                    # Filled
                    QLabel_filled = QLabel('Filled:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_filled.setFont(font)
                    QLabel_filled.setGeometry(5, 110, 100, 35)
                    QLabel_filled.show()
                    # filled checkbox
                    self.filled_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.filled_checkBox.setGeometry(102, 117, 110, 20)
                    self.filled_checkBox.setFont(font)
                    self.filled_checkBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

                case self.Rectangle_checkbox:
                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.object_name_lineEdit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit.show()

                    # Color label
                    QLabel_diameter = QLabel('Color:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_diameter.setFont(font)
                    QLabel_diameter.setGeometry(5, 50, 100, 35)
                    QLabel_diameter.show()
                    # Color LineEdit
                    self.color_lineEdit = QLineEdit(self.chosen_widget_parameters_box)
                    self.color_lineEdit.setGeometry(100, 57, 55, 20)
                    self.color_lineEdit.setStyleSheet("background-color: white; padding: 0px;")
                    self.color_lineEdit.show()
                    # Color Pushbutton
                    self.color_button = QPushButton(self.chosen_widget_parameters_box)
                    self.color_button.setText('Color')
                    self.font = QFont('Arial', 12)
                    self.color_button.setFont(font)
                    self.color_button.setGeometry(160, 55, 50, 25)
                    self.color_button.setStyleSheet("background-color: white; padding: 0px;")
                    self.color_button.show()

                    # connect to choose color dialog
                    self.color_button.clicked.connect(self.choose_color)

                    # Filled
                    QLabel_filled = QLabel('Filled:', self.chosen_widget_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_filled.setFont(font)
                    QLabel_filled.setGeometry(5, 80, 100, 35)
                    QLabel_filled.show()
                    # filled checkbox
                    self.filled_checkBox = QCheckBox(self.chosen_widget_parameters_box)
                    self.filled_checkBox.setGeometry(102, 87, 110, 20)
                    self.filled_checkBox.setFont(font)
                    self.filled_checkBox.show()

                    self.chosen_widget_parameters_box.setFixedHeight(190)

    def update_value_spinbox_range(self, type):
        if type == 'add':
            min_value_spinbox = self.min_value_SpinBox
            max_value_spinBox = self.max_value_SpinBox
            value_spinBox = self.value_SpinBox
        elif type == 'edit':
            min_value_spinbox = self.min_value_SpinBox_update
            max_value_spinBox = self.max_value_SpinBox_update
            value_spinBox = self.value_SpinBox_update
        min_value = min_value_spinbox.value()  # Pobiera wartość minimalną
        max_value = max_value_spinBox.value()  # Pobiera wartość maksymalną

        # Upewnienie się, że min_value nie jest większe niż max_value
        if min_value > max_value:
            # Jeśli min_value jest większe niż max_value, ustaw min_value na max_value
            min_value_spinbox.setValue(max_value)
            min_value = max_value  # Zaktualizowanie min_value, aby były zgodne

        # Ustawienie nowych granic
        value_spinBox.setMinimum(min_value)
        value_spinBox.setMaximum(max_value)

    def update_date_range(self, type):
        if type == 'add':
            min_date_dateEdit = self.min_date_dateEdit
            max_date_dateEdit = self.max_date_dateEdit
            set_date_dateEdit = self.set_date_dateEdit
        elif type == 'edit':
            min_date_dateEdit = self.min_date_dateEdit_update
            max_date_dateEdit = self.max_date_dateEdit_update
            set_date_dateEdit = self.set_date_dateEdit_update
        min_date = min_date_dateEdit.date()  # Pobiera datę minimalną
        max_date = max_date_dateEdit.date()  # Pobiera datę maksymalną

        # Upewnienie się, że min_date nie jest większa niż max_date
        if min_date > max_date:
            # Jeśli min_date jest większa niż max_date, ustaw min_date na max_date
            min_date_dateEdit.setDate(max_date)
            min_date = max_date  # Zaktualizowanie min_date, aby były zgodne

        # Ustawienie nowych granic daty
        set_date_dateEdit.setMinimumDate(min_date)
        set_date_dateEdit.setMaximumDate(max_date)

    def choose_color(self):
        """
        Opens Color Palett dialog
        """
        dialog = QColorDialog()
        selected_color = dialog.getColor()
        selected_color = selected_color.name()
        self.color_lineEdit.clear()
        self.color_lineEdit.insert(selected_color)

    # aktualizacja pozycji kursora
    def update_cursor_position(self):
        cursor_position = QtGui.QCursor.pos()
        self.status_bar.showMessage(f"Pozycja kursora: ({cursor_position.x()}, {cursor_position.y()})")

    # otawrcie okna do tworzenia nowych okien
    def new_window(self):
        dialog = NewWindowDialog(width=self.screen_width, height=self.screen_height)
        dialog.exec()

    # dodanie wybranego widgetu do okna
    def add_widget_to_window(self):
        window_name = self.window_name_comboBox.currentText()
        window_groupbox = self.root_space_groupbox.findChild(QGroupBox, window_name)
        if window_name != '':
            widgets = {
                "x_pos": "X_pos_spinBox",
                "y_pos": "Y_pos_spinBox",
                "width": "width_spinBox",
                "height": "height_spinBox",
                "object_name": "object_name_lineEdit",
                "text": "text_lineEdit",
                "family_font": "font_family_comboBox",
                "family_size": "font_size_SpinBox",
                "bold": "bold_checkBox",
                "min_value": "min_value_SpinBox",
                "max_value": "max_value_SpinBox",
                "value": "value_SpinBox",
                "orientation": "orientation_comboBox",
                "min_date": "min_date_dateEdit",
                "max_date": "max_date_dateEdit",
                "set_date": "set_date_dateEdit",
                "grid": "grid_checkBox",
                "line_width": "widthLine_SpinBox",
                "frame": "frame_comboBox",
                "diameter": "diameter_SpinBox",
                "color": "color_lineEdit",
                "filled": "filled_checkBox",
                "max_visible_items": "max_visible_items_spinBox",
                "read_only": "read_only_checkBox",
                "single_step": "singleStep_SpinBox",
                "prefix": "prefix_lineEdit",
                "suffix": "suffix_lineEdit",
                "decimal": "decimal_SpinBox",
                "cal_popup": "calendar_popup_checkBox",
                "page_step": "pageStep_SpinBox",
                "checkable": "checkable_checkBox",
                "checked": "checked_checkBox",
            }

            values = {}

            for key, widget_name in widgets.items():
                if hasattr(self, widget_name):
                    widget = getattr(self, widget_name)
                    if isinstance(widget, (QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox)):
                        values[key] = widget.value()
                    elif isinstance(widget, QtWidgets.QLineEdit):
                        values[key] = widget.text()
                    elif isinstance(widget, QtWidgets.QComboBox):
                        values[key] = widget.currentText() if widget_name != "font_family_comboBox" else widget.currentFont().family()
                    elif isinstance(widget, QtWidgets.QCheckBox):
                        values[key] = widget.isChecked()
                    elif isinstance(widget, QtWidgets.QDateEdit):
                        values[key] = widget.date()
                else:
                    values[key] = None  # Można zmienić na wartość domyślną

            # wszystkie wartości w słowniku `values`
            x_pos = values["x_pos"]
            y_pos = values["y_pos"]
            width = values["width"]
            height = values["height"]
            object_name = values["object_name"]
            text = values["text"]
            family_font = values["family_font"]
            family_size = values["family_size"]
            bold = values["bold"]
            min_value = values["min_value"]
            max_value = values["max_value"]
            value = values["value"]
            orientation = values["orientation"]
            min_date = values["min_date"]
            max_date = values["max_date"]
            set_date = values["set_date"]
            grid = values["grid"]
            line_width = values["line_width"]
            frame = values["frame"]
            diameter = values["diameter"]
            color = values["color"]
            filled = values["filled"]
            max_visible_items = values["max_visible_items"]
            read_only = values["read_only"]
            single_step = values["single_step"]
            prefix = values["prefix"]
            suffix = values["suffix"]
            decimal = values["decimal"]
            cal_popup = values["cal_popup"]
            page_step = values["page_step"]
            checkable = values["checkable"]
            checked = values["checked"]

            window_name = self.window_name_comboBox.currentText()
            found_group_box = main_window.root_space_groupbox.findChild(QGroupBox, window_name)
            object_names_list = []
            if found_group_box is not None:
                for child in found_group_box.findChildren(QWidget):
                    if child.objectName() != '':
                        object_names_list.append(child.objectName())

            if object_name in object_names_list:
                QMessageBox.critical(self, 'Error', 'Object name has to be unique!')
                return
            elif object_name == '':
                QMessageBox.critical(self, 'Error', 'Insert Object Name!')
                return

            if self.QLabel_checkbox.isChecked() == True:
                # stworzenie labela
                Label = QLabel(text, window_groupbox)
                font = QFont(family_font, family_size)
                font.setBold(bold)
                Label.setFont(font)
                Label.setGeometry(x_pos, y_pos, width, height)
                Label.setObjectName(object_name)
                Label.show()
            elif self.Progressbar_checkbox.isChecked() == True:
                ProgressBar = QProgressBar(window_groupbox)
                ProgressBar.setGeometry(x_pos, y_pos, width, height)
                ProgressBar.setMinimum(min_value)
                ProgressBar.setMaximum(max_value)
                ProgressBar.setValue(value)
                if orientation == 'Horizontal':
                    ProgressBar.setOrientation(Qt.Orientation.Horizontal)
                elif orientation == 'Vertical':
                    ProgressBar.setOrientation(Qt.Orientation.Vertical)
                ProgressBar.setObjectName(object_name)
                ProgressBar.setEnabled(False)
                ProgressBar.show()
            elif self.Calendar_checkbox.isChecked() == True:
                Calendar = QCalendarWidget(window_groupbox)
                Calendar.setGeometry(x_pos, y_pos, width, height)
                Calendar.setMinimumDate(min_date)
                Calendar.setMaximumDate(max_date)
                Calendar.setSelectedDate(set_date)
                Calendar.setObjectName(object_name)
                Calendar.setGridVisible(grid)
                Calendar.setEnabled(False)
                Calendar.show()
            elif self.Horizontal_line_checkbox.isChecked() == True:
                Horizontal_line = QFrame(window_groupbox)
                Horizontal_line.setFrameShape(QFrame.Shape.HLine)  # Ustawienie kształtu na poziomą linię
                if frame == 'Plain':
                    Horizontal_line.setFrameShadow(QFrame.Shadow.Plain)
                elif frame == 'Raised':
                    Horizontal_line.setFrameShadow(QFrame.Shadow.Raised)
                elif frame == 'Sunken':
                    Horizontal_line.setFrameShadow(QFrame.Shadow.Sunken)
                Horizontal_line.setGeometry(x_pos, y_pos, width, height)
                Horizontal_line.setObjectName(object_name)
                Horizontal_line.setStyleSheet(f"background-color: white")
                Horizontal_line.setLineWidth(line_width)
                Horizontal_line.setEnabled(False)
                Horizontal_line.show()
            elif self.Vertical_line_checkbox.isChecked() == True:
                Vertical_line = QFrame(window_groupbox)
                Vertical_line.setFrameShape(QFrame.Shape.VLine)  # Ustawienie kształtu na pionowa linię
                if frame == 'Plain':
                    Vertical_line.setFrameShadow(QFrame.Shadow.Plain)
                elif frame == 'Raised':
                    Vertical_line.setFrameShadow(QFrame.Shadow.Raised)
                elif frame == 'Sunken':
                    Vertical_line.setFrameShadow(QFrame.Shadow.Sunken)
                Vertical_line.setGeometry(x_pos, y_pos, width, height)
                Vertical_line.setObjectName(object_name)
                Vertical_line.setStyleSheet(f"background-color: white")
                Vertical_line.setLineWidth(line_width)
                Vertical_line.setEnabled(False)
                Vertical_line.show()
            elif self.Cirlce_checkbox.isChecked() == True:
                Circle = CircleWidget(x=x_pos, y=y_pos, diameter=diameter, color=QColor(color), filled=filled, object_name=object_name, width=width, height=height, parent=window_groupbox)
                Circle.show()
            elif self.Rectangle_checkbox.isChecked() == True:
                Rectangle = RectangleWidget(x=x_pos, y=y_pos, width=width, height=height, color=QColor(color), filled=filled, object_name=object_name, parent=window_groupbox)
                Rectangle.show()
            elif self.QComboBox_checkbox.isChecked() == True:
                ComboBox = QComboBox(window_groupbox)
                ComboBox.setGeometry(x_pos, y_pos, width, height)
                ComboBox.setMaxVisibleItems(max_visible_items)
                ComboBox.setObjectName(object_name)
                ComboBox.setEnabled(False)
                ComboBox.show()
            elif self.QLineEdit_checkbox.isChecked() == True:
                LineEdit = QLineEdit(window_groupbox)
                LineEdit.setGeometry(x_pos, y_pos, width, height)
                LineEdit.setText(text)
                font = QFont(family_font, family_size)
                LineEdit.setFont(font)
                LineEdit.setReadOnly(read_only)
                LineEdit.setObjectName(object_name)
                LineEdit.setEnabled(False)
                LineEdit.show()
            elif self.QSpinBox_checkbox.isChecked() == True:
                SpinBox = QSpinBox(window_groupbox)
                SpinBox.setGeometry(x_pos, y_pos, width, height)
                SpinBox.setMinimum(min_value)
                SpinBox.setMaximum(max_value)
                SpinBox.setValue(value)
                SpinBox.setSingleStep(single_step)
                SpinBox.setPrefix(prefix)
                SpinBox.setSuffix(suffix)
                SpinBox.setObjectName(object_name)
                SpinBox.setEnabled(False)
                SpinBox.show()
            elif self.QDoubleSpinBox_checkbox.isChecked() == True:
                DoubleSpinBox = QDoubleSpinBox(window_groupbox)
                DoubleSpinBox.setGeometry(x_pos, y_pos, width, height)
                DoubleSpinBox.setMinimum(min_value)
                DoubleSpinBox.setMaximum(max_value)
                DoubleSpinBox.setValue(value)
                DoubleSpinBox.setSingleStep(single_step)
                DoubleSpinBox.setDecimals(decimal)
                DoubleSpinBox.setPrefix(prefix)
                DoubleSpinBox.setSuffix(suffix)
                DoubleSpinBox.setObjectName(object_name)
                DoubleSpinBox.setEnabled(False)
                DoubleSpinBox.show()
            elif self.QDateEdit_checkbox.isChecked() == True:
                DateEedit = QDateEdit(window_groupbox)
                DateEedit.setGeometry(x_pos, y_pos, width, height)
                DateEedit.setMinimumDate(min_date)
                DateEedit.setMaximumDate(max_date)
                DateEedit.setDate(set_date)
                DateEedit.setCalendarPopup(cal_popup)
                DateEedit.setObjectName(object_name)
                DateEedit.setEnabled(False)
                DateEedit.show()
            elif self.QHorizontalSlider_checkbox.isChecked() == True:
                HorizontalSlider = QSlider(window_groupbox)
                HorizontalSlider.setOrientation(Qt.Orientation.Horizontal)
                HorizontalSlider.setGeometry(x_pos, y_pos, width, height)
                HorizontalSlider.setMinimum(min_value)
                HorizontalSlider.setMaximum(max_value)
                HorizontalSlider.setValue(value)
                HorizontalSlider.setSingleStep(single_step)
                HorizontalSlider.setPageStep(page_step)
                HorizontalSlider.setObjectName(object_name)
                HorizontalSlider.setEnabled(False)
                HorizontalSlider.show()
            elif self.QVerticalSilder_checkbox.isChecked() == True:
                VerticalSlider = QSlider(window_groupbox)
                VerticalSlider.setOrientation(Qt.Orientation.Vertical)
                VerticalSlider.setGeometry(x_pos, y_pos, width, height)
                VerticalSlider.setMinimum(min_value)
                VerticalSlider.setMaximum(max_value)
                VerticalSlider.setValue(value)
                VerticalSlider.setSingleStep(single_step)
                VerticalSlider.setPageStep(page_step)
                VerticalSlider.setObjectName(object_name)
                VerticalSlider.setEnabled(False)
                VerticalSlider.show()
            elif self.QPushButton_checkbox.isChecked() == True:
                PushButton = QPushButton(window_groupbox)
                PushButton.setGeometry(x_pos, y_pos, width, height)
                PushButton.setText(text)
                PushButton.setCheckable(checkable)
                PushButton.setChecked(checked)
                PushButton.setObjectName(object_name)
                PushButton.setEnabled(False)
                PushButton.show()
            elif self.QCheckBox_checkbox.isChecked() == True:
                CheckBox = QCheckBox(window_groupbox)
                CheckBox.setGeometry(x_pos, y_pos, width, height)
                CheckBox.setText(text)
                font = QFont(family_font, family_size)
                CheckBox.setFont(font)
                CheckBox.setCheckable(checkable)
                CheckBox.setChecked(checked)
                CheckBox.setObjectName(object_name)
                CheckBox.setEnabled(False)
                CheckBox.show()
            else:
                QMessageBox.critical(self, 'Error', 'Select widget before!')

            self.update_object_name_to_delete_comboBox()
            self.update_object_name_to_update_comboBox()
        else:
            QMessageBox.critical(self, 'Error', 'Create window before!')

    # dodanie czerwonego obramowania do widgetu
    def widget_to_delete_changed(self):
        windows_list = main_window.root_space_groupbox.findChildren(QGroupBox)
        for window in windows_list:
            widgets_list = window.findChildren(QWidget)
            for widget in widgets_list:
                if type(widget) == CircleWidget or type(widget) == RectangleWidget:
                    widget.hide_red_border()
                    widget.hide_green_border()
                else:
                    widget.setStyleSheet("border: none;")

        object_name = self.object_name_delete_comboBox.currentText()
        window_name = self.window_name_delete_comboBox.currentText()
        window = self.root_space_groupbox.findChild(QGroupBox, window_name)

        if window is not None:
            widget_to_delete = window.findChild(QWidget, object_name)
            if widget_to_delete is not None:
                if type(widget_to_delete) == CircleWidget or type(widget_to_delete) == RectangleWidget:
                    widget_to_delete.toggle_red_border()
                else:
                    widget_to_delete.setStyleSheet("border: 1px solid red;")

        object_name = self.object_name_update_comboBox.currentText()
        window_name = self.window_name_update_comboBox.currentText()
        window = main_window.root_space_groupbox.findChild(QGroupBox, window_name)

        if window is not None:
            widget_to_update = window.findChild(QWidget, object_name)
            if widget_to_update is not None:
                if type(widget_to_update) == CircleWidget or type(widget_to_update) == RectangleWidget:
                    widget_to_update.toggle_green_border()
                else:
                    widget_to_update.setStyleSheet("border: 1px solid green;")

    # dodanie zielonego obramowania do widegtu
    def widget_to_update_changed(self):
        object_name = self.object_name_update_comboBox.currentText()
        window_name = self.window_name_update_comboBox.currentText()
        window = main_window.root_space_groupbox.findChild(QGroupBox, window_name)

        if window is not None:
            widget_to_update = window.findChild(QWidget, object_name)
            # wyczyszczenie groupboxa
            for child in self.chosen_widget_update_parameters_box.findChildren(QWidget):  # Znajdź wszystkie widgety wewnątrz
                child.setParent(None)  # Odłącz od rodzica, Qt sam go usunie
            if widget_to_update is not None:
                widget_type = type(widget_to_update)
                # geometry
                x, y, width, height = widget_to_update.geometry().getRect()
                self.X_pos_update_spinBox.setValue(x)
                self.Y_pos_update_spinBox.setValue(y)
                self.width_update_spinBox.setValue(width)
                self.height_update_spinBox.setValue(height)
                if widget_type == QLabel:
                    object_name = widget_to_update.objectName()
                    text = widget_to_update.text()
                    font_old = widget_to_update.font()

                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit_update = QLineEdit(self.chosen_widget_update_parameters_box)
                    self.object_name_lineEdit_update.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit_update.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit_update.setText(object_name)
                    self.object_name_lineEdit_update.show()

                    # Text Label
                    QLabel_text = QLabel('Text:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_text.setFont(font)
                    QLabel_text.setGeometry(5, 50, 100, 35)
                    QLabel_text.show()
                    # Text lineEdit
                    self.text_lineEdit_edit = QLineEdit(self.chosen_widget_update_parameters_box)
                    self.text_lineEdit_edit.setGeometry(100, 57, 110, 20)
                    self.text_lineEdit_edit.setStyleSheet("background-color: white; padding: 0px;")
                    self.text_lineEdit_edit.setText(text)
                    self.text_lineEdit_edit.show()

                    # Font Label
                    QLabel_font_family = QLabel('Family Font:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_font_family.setFont(font)
                    QLabel_font_family.setGeometry(5, 80, 100, 35)
                    QLabel_font_family.show()
                    # font family ComboBox
                    self.font_family_comboBox_update = QFontComboBox(self.chosen_widget_update_parameters_box)
                    self.font_family_comboBox_update.setGeometry(100, 87, 110, 20)
                    self.font_family_comboBox_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.font_family_comboBox_update.setEditable(False)
                    self.font_family_comboBox_update.setCurrentFont(font_old)
                    self.font_family_comboBox_update.show()

                    # Font size
                    QLabel_font_size = QLabel('Family Size:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_font_size.setFont(font)
                    QLabel_font_size.setGeometry(5, 110, 100, 35)
                    QLabel_font_size.show()
                    # font Size SpinBox
                    self.font_size_SpinBox_update = QSpinBox(self.chosen_widget_update_parameters_box)
                    self.font_size_SpinBox_update.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.font_size_SpinBox_update.setFont(font)
                    self.font_size_SpinBox_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.font_size_SpinBox_update.setMinimum(1)
                    self.font_size_SpinBox_update.setMaximum(100)
                    self.font_size_SpinBox_update.setValue(font_old.pointSize())
                    self.font_size_SpinBox_update.show()

                    # Bold
                    QLabel_bold = QLabel('Bold:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_bold.setFont(font)
                    QLabel_bold.setGeometry(5, 140, 100, 35)
                    QLabel_bold.show()
                    # Bold Checkbox
                    self.bold_checkBox_update = QCheckBox(self.chosen_widget_update_parameters_box)
                    self.bold_checkBox_update.setGeometry(102, 147, 110, 20)
                    self.bold_checkBox_update.setFont(font)
                    self.bold_checkBox_update.setChecked(font_old.bold())
                    self.bold_checkBox_update.show()

                    self.chosen_widget_update_parameters_box.setFixedHeight(190)
                elif widget_type == QProgressBar:
                    object_name = widget_to_update.objectName()
                    min_value = widget_to_update.minimum()
                    max_value = widget_to_update.maximum()
                    value = widget_to_update.value()
                    orientation = widget_to_update.orientation()

                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit_edit = QLineEdit(self.chosen_widget_update_parameters_box)
                    self.object_name_lineEdit_edit.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit_edit.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit_edit.setText(object_name)
                    self.object_name_lineEdit_edit.show()

                    # Min value Label
                    QLabel_min_value = QLabel('Min Value:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_value.setFont(font)
                    QLabel_min_value.setGeometry(5, 50, 100, 35)
                    QLabel_min_value.show()
                    # Min value SpinBox
                    self.min_value_SpinBox_update = QSpinBox(self.chosen_widget_update_parameters_box)
                    self.min_value_SpinBox_update.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 9)
                    self.min_value_SpinBox_update.setFont(font)
                    self.min_value_SpinBox_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_value_SpinBox_update.setMinimum(-99999)
                    self.min_value_SpinBox_update.setMaximum(99999)
                    self.min_value_SpinBox_update.setValue(min_value)
                    self.min_value_SpinBox_update.show()

                    # Max value Label
                    QLabel_max_value = QLabel('Max Value:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_value.setFont(font)
                    QLabel_max_value.setGeometry(5, 80, 100, 35)
                    QLabel_max_value.show()
                    # Max value SpinBox
                    self.max_value_SpinBox_update = QSpinBox(self.chosen_widget_update_parameters_box)
                    self.max_value_SpinBox_update.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 9)
                    self.max_value_SpinBox_update.setFont(font)
                    self.max_value_SpinBox_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_value_SpinBox_update.setMinimum(-99999)
                    self.max_value_SpinBox_update.setMaximum(99999)
                    self.max_value_SpinBox_update.setValue(max_value)
                    self.max_value_SpinBox_update.show()

                    # Value Label
                    QLabel_value = QLabel('Value:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_value.setFont(font)
                    QLabel_value.setGeometry(5, 110, 100, 35)
                    QLabel_value.show()
                    # Value SpinBox
                    self.value_SpinBox_update = QSpinBox(self.chosen_widget_update_parameters_box)
                    self.value_SpinBox_update.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 9)
                    self.value_SpinBox_update.setFont(font)
                    self.value_SpinBox_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.value_SpinBox_update.setValue(value)
                    self.value_SpinBox_update.show()

                    # Połączenie sygnałów zmiany wartości min/max SpinBoxa
                    self.min_value_SpinBox_update.valueChanged.connect(lambda: self.update_value_spinbox_range(type='edit'))
                    self.max_value_SpinBox_update.valueChanged.connect(lambda: self.update_value_spinbox_range(type='edit'))

                    # Ustawienie domyślnego zakres
                    self.update_value_spinbox_range(type='edit')

                    # Orientation Label
                    QLabel_orientation = QLabel('Orientation:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_orientation.setFont(font)
                    QLabel_orientation.setGeometry(5, 140, 100, 35)
                    QLabel_orientation.show()
                    # Orientation ComboBox
                    self.orientation_comboBox_update = QComboBox(self.chosen_widget_update_parameters_box)
                    self.orientation_comboBox_update.setGeometry(100, 147, 110, 20)
                    font = QFont('Arial', 8)
                    self.orientation_comboBox_update.setFont(font)
                    self.orientation_comboBox_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.orientation_comboBox_update.addItem('Horizontal')
                    self.orientation_comboBox_update.addItem('Vertical')
                    if orientation == Qt.Orientation.Vertical:
                        self.orientation_comboBox_update.setCurrentText('Vertical')
                    elif orientation == Qt.Orientation.Horizontal:
                        self.orientation_comboBox_update.setCurrentText('Horizontal')
                    self.orientation_comboBox_update.show()

                    self.chosen_widget_update_parameters_box.setFixedHeight(190)
                elif widget_type == QCalendarWidget:
                    object_name = widget_to_update.objectName()
                    min_date = widget_to_update.minimumDate()
                    max_date = widget_to_update.maximumDate()
                    date_old = widget_to_update.selectedDate()
                    grid = widget_to_update.isGridVisible()

                    # Object Name Label
                    QLabel_object_name = QLabel('Object Name:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_object_name.setFont(font)
                    QLabel_object_name.setGeometry(5, 20, 100, 35)
                    QLabel_object_name.show()
                    # Object Name lineEdit
                    self.object_name_lineEdit_update = QLineEdit(self.chosen_widget_update_parameters_box)
                    self.object_name_lineEdit_update.setGeometry(100, 27, 110, 20)
                    self.object_name_lineEdit_update.setStyleSheet("background-color: white; padding: 0px;")
                    self.object_name_lineEdit_update.setText(object_name)
                    self.object_name_lineEdit_update.show()

                    # Min date Label
                    QLabel_min_date = QLabel('Min Date:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_min_date.setFont(font)
                    QLabel_min_date.setGeometry(5, 50, 100, 35)
                    QLabel_min_date.show()
                    # Min value DateEdit
                    self.min_date_dateEdit_update = QDateEdit(self.chosen_widget_update_parameters_box)
                    self.min_date_dateEdit_update.setGeometry(100, 57, 110, 20)
                    font = QFont('Arial', 8)
                    self.min_date_dateEdit_update.setFont(font)
                    self.min_date_dateEdit_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.min_date_dateEdit_update.setMinimumDate(QDate(1000, 1, 1))
                    self.min_date_dateEdit_update.setMaximumDate(QDate(9999, 12, 31))
                    self.min_date_dateEdit_update.setDate(min_date)
                    self.min_date_dateEdit_update.show()

                    # Max date Label
                    QLabel_max_date = QLabel('Max Date:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_max_date.setFont(font)
                    QLabel_max_date.setGeometry(5, 80, 100, 35)
                    QLabel_max_date.show()
                    # Min value DateEdit
                    self.max_date_dateEdit_update = QDateEdit(self.chosen_widget_update_parameters_box)
                    self.max_date_dateEdit_update.setGeometry(100, 87, 110, 20)
                    font = QFont('Arial', 8)
                    self.max_date_dateEdit_update.setFont(font)
                    self.max_date_dateEdit_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.max_date_dateEdit_update.setMinimumDate(QDate(1000, 1, 1))
                    self.max_date_dateEdit_update.setMaximumDate(QDate(9999, 12, 31))
                    self.max_date_dateEdit_update.setDate(max_date)
                    self.max_date_dateEdit_update.setCalendarPopup(True)
                    self.max_date_dateEdit_update.show()

                    # Set date Label
                    QLabel_set_date = QLabel('Set Date:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_set_date.setFont(font)
                    QLabel_set_date.setGeometry(5, 110, 100, 35)
                    QLabel_set_date.show()
                    # Set date DateEdit
                    self.set_date_dateEdit_update = QDateEdit(self.chosen_widget_update_parameters_box)
                    self.set_date_dateEdit_update.setGeometry(100, 117, 110, 20)
                    font = QFont('Arial', 8)
                    self.set_date_dateEdit_update.setFont(font)
                    self.set_date_dateEdit_update.setStyleSheet("background-color: white; padding: 1px 10px;")
                    self.set_date_dateEdit_update.setMinimumDate(QDate(1000, 1, 1))
                    self.set_date_dateEdit_update.setMaximumDate(QDate(9999, 12, 31))
                    self.set_date_dateEdit_update.setDate(date_old)
                    self.set_date_dateEdit_update.setCalendarPopup(True)
                    self.set_date_dateEdit_update.show()

                    self.min_date_dateEdit_update.dateChanged.connect(lambda: self.update_date_range(type='edit'))
                    self.max_date_dateEdit_update.dateChanged.connect(lambda: self.update_date_range(type='edit'))

                    # Grid Visible Label
                    QLabel_grid = QLabel('Grid Visible:', self.chosen_widget_update_parameters_box)
                    font = QFont('Arial', 10)
                    QLabel_grid.setFont(font)
                    QLabel_grid.setGeometry(5, 140, 100, 35)
                    QLabel_grid.show()
                    # Grid Visible Checkbox
                    self.grid_checkBox_update = QCheckBox(self.chosen_widget_update_parameters_box)
                    self.grid_checkBox_update.setGeometry(102, 147, 110, 20)
                    self.grid_checkBox_update.setFont(font)
                    self.grid_checkBox_update.setChecked(grid)
                    self.grid_checkBox_update.show()

                    self.chosen_widget_update_parameters_box.setFixedHeight(190)


    # usuwanie wybranego widgetu z okna
    def delete_widget(self):
        object_name = self.object_name_delete_comboBox.currentText()
        window_name = self.window_name_delete_comboBox.currentText()
        window = main_window.root_space_groupbox.findChild(QGroupBox, window_name)
        if window is not None and object_name != '':
            widget_to_delete = window.findChild(QWidget, object_name)
            if widget_to_delete is not None:
                widget_to_delete.setParent(None)
                widget_to_delete.deleteLater()

            self.update_object_name_to_delete_comboBox()
            self.update_object_name_to_update_comboBox()

    # aktualizacja object name to delete comboBox
    def update_object_name_to_delete_comboBox(self):
        window_name = self.window_name_delete_comboBox.currentText()

        main_window.object_name_delete_comboBox.clear()
        main_window.object_name_delete_comboBox.addItem('')
        found_group_box = main_window.root_space_groupbox.findChild(QGroupBox, window_name)
        if found_group_box is not None:
            for child in found_group_box.findChildren(QWidget):
                if child.parent() == found_group_box and child.objectName() and not isinstance(child, DottedWidget):
                    main_window.object_name_delete_comboBox.addItem(child.objectName())

    # aktualizacja object name to update comboBox
    def update_object_name_to_update_comboBox(self):
        window_name = self.window_name_update_comboBox.currentText()

        main_window.object_name_update_comboBox.clear()
        main_window.object_name_update_comboBox.addItem('')
        found_group_box = main_window.root_space_groupbox.findChild(QGroupBox, window_name)
        if found_group_box is not None:
            for child in found_group_box.findChildren(QWidget):
                if child.parent() == found_group_box and child.objectName() and not isinstance(child, DottedWidget):
                    main_window.object_name_update_comboBox.addItem(child.objectName())


# oknko do tworzenia nowych okien
class NewWindowDialog(QDialog):
    def __init__(self, width, height):
        super(NewWindowDialog, self).__init__()

        # ustawienie wielkości okna
        self.setGeometry(int(width/2.5), int(height/2.5), 225, 250)

        # Label 'Window Name'
        self.window_name_label = QLabel(self)
        self.window_name_label.setText('Window Name:')
        font = QFont("Arial", 12)
        self.window_name_label.setFont(font)
        self.window_name_label.setGeometry(20, 5, 120, 25)
        # Line Edit 'Window Name'
        self.window_name_lineEdit = QLineEdit(self)
        self.window_name_lineEdit.setGeometry(140, 5, 80, 25)
        self.window_name_lineEdit.setStyleSheet("border: 1px solid red;")
        self.window_name_lineEdit.textChanged.connect(self.window_name_changed)

        # Label 'X pos'
        self.x_pos_label = QLabel(self)
        self.x_pos_label.setText('X pos:')
        font = QFont("Arial", 12)
        self.x_pos_label.setFont(font)
        self.x_pos_label.setGeometry(20, 45, 60, 25)
        # Spinbox 'X pos'
        self.x_pos_spinbox = QSpinBox(self)
        self.x_pos_spinbox.setMaximum(width)
        self.x_pos_spinbox.setSuffix(' pxl')
        self.x_pos_spinbox.setGeometry(80, 45, 30, 25)

        # Label 'y pos'
        self.y_pos_label = QLabel(self)
        self.y_pos_label.setText('Y pos:')
        font = QFont("Arial", 12)
        self.y_pos_label.setFont(font)
        self.y_pos_label.setGeometry(20, 85, 60, 25)
        # Spinbox 'Y pos'
        self.y_pos_spinbox = QSpinBox(self)
        self.y_pos_spinbox.setMaximum(height)
        self.y_pos_spinbox.setSuffix(' pxl')
        self.y_pos_spinbox.setGeometry(80, 85, 30, 25)

        # Label 'Width'
        self.width_label = QLabel(self)
        self.width_label.setText('Width:')
        font = QFont("Arial", 12)
        self.width_label.setFont(font)
        self.width_label.setGeometry(20, 125, 60, 25)
        # Spinbox 'Width'
        self.width_spinbox = QSpinBox(self)
        self.width_spinbox.setMaximum(width)
        self.width_spinbox.setSuffix(' pxl')
        self.width_spinbox.setGeometry(80, 125, 30, 25)

        # Label 'Height'
        self.height_label = QLabel(self)
        self.height_label.setText('Height:')
        font = QFont("Arial", 12)
        self.height_label.setFont(font)
        self.height_label.setGeometry(20, 165, 60, 25)
        # Spinbox 'Width'
        self.height_spinbox = QSpinBox(self)
        self.height_spinbox.setMaximum(height)
        self.height_spinbox.setSuffix(' pxl')
        self.height_spinbox.setGeometry(80, 165, 30, 25)

        # create button
        self.create_button = QPushButton(self)
        self.create_button.setText('Create')
        self.font = QFont('Arial', 12)
        self.create_button.setFont(font)
        self.create_button.setGeometry(80, 205, 70, 30)

        self.create_button.clicked.connect(lambda: self.create_window(x=self.x_pos_spinbox.value(), y=self.y_pos_spinbox.value(),
                                                                 width=self.width_spinbox.value(), height=self.height_spinbox.value(),
                                                                 name=self.window_name_lineEdit.text()))

    def create_window(self, x, y, width, height, name):
        """Dodaje nową QScrollArea do interfejsu i zapisuje do pliku."""
        window_list = []
        for window in main_window.root_space_groupbox.findChildren(QGroupBox):
            window_list.append(window.objectName())

        if name in window_list:
            QMessageBox.critical(self, 'Error', 'Window name has to be unique!')
            return

        if name != '':
            # stworzenie przestrzeni roboczej (prostokąt)
            main_root_space_groupbox = main_window.findChild(QGroupBox, 'root_space_groupbox')

            new_window = QGroupBox(name, main_root_space_groupbox)
            new_window.setGeometry(x, y, width, height)
            new_window.setStyleSheet("background-color: white; padding: 10px;")
            new_window.setObjectName(name)

            # Tworzenie kropkowanego widgetu
            dotted_widget = DottedWidget()
            dotted_widget.setObjectName('Dotted')
            dotted_widget.setParent(new_window)  # Ustawienie rodzica
            dotted_widget.setGeometry(0, 0, width, height)  # Dopasowanie do QGroupBox

            main_window.window_name_comboBox.clear()
            main_window.window_name_delete_comboBox.clear()
            main_window.window_name_update_comboBox.clear()
            windows_list = main_window.root_space_groupbox.findChildren(QGroupBox)
            for window in windows_list:
                name = window.objectName()
                main_window.window_name_comboBox.addItem(name)
                main_window.window_name_delete_comboBox.addItem(name)
                main_window.window_name_update_comboBox.addItem(name)

            new_window.show()
        else:
            QMessageBox.critical(self, 'Error', 'Insert Window Name!')

    def window_name_changed(self):
        if self.window_name_lineEdit.text() == '':
            self.window_name_lineEdit.setStyleSheet("border: 1px solid red;")
        else:
            self.window_name_lineEdit.setStyleSheet("border: 1px solid green;")


if __name__ == "__main__":
    generic.close_splash()
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec())

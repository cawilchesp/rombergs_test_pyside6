"""
PyQt Components adapted to follow Material Design 3 guidelines


"""

from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt

import sys

light = {
    'background': '#E5E9F0',
    'surface': '#B2B2B2',
    'primary': '#42A4F5',
    'secondary': '#FF2D55',
    'on_background': '#000000',
    'on_surface': '#000000',
    'on_primary': '#000000',
    'on_secondary': '#000000',
    'disable': '#B2B2B2',
    'error': ''
}

dark = {
    'background': '#3B4253',
    'surface': '#2E3441',
    'primary': '#42A4F5',
    'secondary': '#FF2D55',
    'on_background': '#E5E9F0',
    'on_surface': '#E5E9F0',
    'on_primary': '#000000',
    'on_secondary': '#000000',
    'disable': '#B2B2B2',
    'error': ''
}

current_path = sys.path[0].replace('\\','/')

# ----
# Card
# ----
class Card(QtWidgets.QFrame):
    def __init__(self, parent, name, geometry, labels, theme, language):
        super(Card, self).__init__(parent)
        
        self.name = name
        self.label_es, self.label_en = labels
        x, y, w, h = geometry

        self.setObjectName(self.name)
        self.setGeometry(x, y, w, h)

        self.title = QtWidgets.QLabel(self)
        self.title.setGeometry(8, 8, w-16, 32)
        self.title.setFont(QtGui.QFont('Segoe UI', 14))

        self.apply_styleSheet(theme)
        self.language_text(language)
    
    def apply_styleSheet(self, theme):
        if theme:
            background_color = light["surface"]
            color = light["on_surface"]
        else:
            background_color = dark["surface"]
            color = dark["on_surface"]
        self.setStyleSheet(f'QFrame#{self.name} {{ border-radius: 16px;'
                 f'background-color: {background_color} }}'
                 f'QLabel {{ background-color: {background_color}; color: {color} }}')

    def language_text(self, language):
        if language == 0:   self.title.setText(self.label_es)
        elif language == 1: self.title.setText(self.label_en)

# ----------
# Item Label
# ----------
class ItemLabel(QtWidgets.QLabel):
    def __init__(self, parent, name, labels, geometry, theme, language):
        super(ItemLabel, self).__init__(parent)

        self.name = name
        self.label_es, self.label_en = labels
        x, y = geometry

        self.setObjectName(self.name)
        self.setGeometry(x, y, parent.geometry().width()-16, 20)
        self.setFont(QtGui.QFont('Segoe UI', 9, QtGui.QFont.Weight.Bold))
        
        self.apply_styleSheet(theme)
        self.language_text(language)
    
    def apply_styleSheet(self, theme):
        if theme:
            background_color = light["surface"]
            color = light["on_surface"]
        else:
            background_color = dark["surface"]
            color = dark["on_surface"]
        self.setStyleSheet(f'QLabel#{self.name} {{ background-color: {background_color};'
                 f'color: {color} }}')

    def language_text(self, language):
        if language == 0:   self.setText(self.label_es)
        elif language == 1: self.setText(self.label_en)

# -----------
# Value Label
# -----------
class ValueLabel(QtWidgets.QLabel):
    def __init__(self, parent, name, geometry, theme):
        super(ValueLabel, self).__init__(parent)

        self.name = name
        x, y, w = geometry

        self.setObjectName(self.name)
        self.setGeometry(x, y, w, 32)
        
        self.apply_styleSheet(theme)
    
    def apply_styleSheet(self, theme):
        if theme:
            background_color = light["surface"]
            color = light["on_surface"]
        else:
            background_color = dark["surface"]
            color = dark["on_surface"]
        self.setStyleSheet(f'QLabel#{self.name} {{ background-color: {background_color};'
                 f'color: {color} }}')
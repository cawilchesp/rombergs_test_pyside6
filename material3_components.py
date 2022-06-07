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
    def __init__(self, parent, object_name, geometry, labels, style, language):
        super(Card, self).__init__(parent)
        
        self.object_name = object_name
        self.text_es, self.text_en = labels
        x, y, w, h = geometry

        self.setObjectName(self.object_name)
        self.setGeometry(x, y, w, h)

        self.title = QtWidgets.QLabel(self)
        self.title.setGeometry(8, 8, w-16, 32)
        self.title.setFont(QtGui.QFont('Segoe UI', 14))

        self.apply_styleSheet(style)
        self.language_text(language)
    
    def apply_styleSheet(self, style):
        if style:
            card_style = (f'QFrame {{ border-radius: 16px;'
                f'background-color: {light["surface"]} }}'
                f'QLabel {{ '
                f'background-color: {light["surface"]};'
                f'color: {light["on_surface"]} }}')
        else:
            card_style = (f'QFrame {{ border-radius: 16px;'
                f'background-color: {dark["surface"]} }}'
                f'QLabel {{ '
                f'background-color: {dark["surface"]};'
                f'color: {dark["on_surface"]} }}')
        self.setStyleSheet(card_style)

    def language_text(self, language):
        if language == 0:
            self.title.setText(self.text_es)
        elif language == 1:
            self.title.setText(self.text_en)
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

current_path = sys.path[0].replace("\\","/")
images_path = f'{current_path}/images'

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

# ----------
# Icon Label
# ----------
class IconLabel(QtWidgets.QLabel):
    def __init__(self, parent, name, geometry, icon, theme):
        super(IconLabel, self).__init__(parent)

        self.name = name
        x, y = geometry

        self.setObjectName(self.name)
        self.setGeometry(x, y, 32, 32)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.set_icon(icon, theme)
        self.apply_styleSheet(theme)

    def set_icon(self, icon, theme):
        if theme: self.setPixmap(QtGui.QIcon(f'{images_path}/{icon}_L.png').pixmap(24))
        else: self.setPixmap(QtGui.QIcon(f'{images_path}/{icon}_D.png').pixmap(24))

    def apply_styleSheet(self, theme):
        if theme:
            background_color = light["surface"]
            color = light["on_surface"]
        else:
            background_color = dark["surface"]
            color = dark["on_surface"]
        self.setStyleSheet(f'QLabel#{self.name} {{ background-color: {background_color};'
                f'color: {color} }}')

# -----------
# Color Label
# -----------
class ColorLabel(QtWidgets.QLabel):
    def __init__(self, parent, name, geometry, color):
        super(ColorLabel, self).__init__(parent)

        self.name = name
        x, y = geometry

        self.setObjectName(self.name)
        self.setGeometry(x, y, 32, 32)
        self.set_color(color)

    def set_color(self, color):
        self.setStyleSheet(f'QLabel#{self.name} {{ border: 2px solid {light["secondary"]};'
            f'border-radius: 15px; background-color: rgb({color}) }}')

# -----------
# Field Label
# -----------
class FieldLabel(QtWidgets.QLabel):
    def __init__(self, parent, name, geometry, labels, theme, language):
        super(FieldLabel, self).__init__(parent)

        self.name = name
        self.label_es, self.label_en = labels
        x, y = geometry

        self.setObjectName(self.name)
        self.setGeometry(x, y, 16, 16)

        self.apply_styleSheet(theme)
        self.language_text(language)
    
    def apply_styleSheet(self, theme):
        if theme:
            background_color = light["surface"]
            color = light["on_surface"]
        else:
            background_color = dark["surface"]
            color = dark["on_surface"]
        self.setStyleSheet(f'QLabel#{self.name} {{ border: 0px solid;'
                f'background-color: {background_color};'
                f'color: {color} }}')

    def language_text(self, language):
        if language == 0:   self.setText(self.label_es)
        elif language == 1: self.setText(self.label_en)
        self.adjustSize()

# -----------
# Text Button
# -----------
class TextButton(QtWidgets.QToolButton):
    def __init__(self, parent, name, geometry, labels, icon, theme, language):
        super(TextButton, self).__init__(parent)

        self.name = name
        self.label_es, self.label_en = labels
        x, y, w = geometry

        self.setObjectName(self.name)
        self.setGeometry(x, y, w, 32)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setAutoRaise(True)
        self.setIcon(QtGui.QIcon(f'{images_path}/{icon}'))

        self.apply_styleSheet(theme)
        self.language_text(language)
        
    def apply_styleSheet(self, theme):
        if theme:
            background_color = light["primary"]
            color = light["on_primary"]
            hover_background_color = light["secondary"]
            hover_color = light["on_secondary"]
        else:
            background_color = dark["primary"]
            color = dark["on_primary"]
            hover_background_color = dark["secondary"]
            hover_color = dark["on_secondary"]
        self.setStyleSheet(f'QToolButton#{self.name} {{ border: 0px solid; border-radius: 16;'
                f'padding: 0 8 0 8; background-color: {background_color};'
                f'color: {color} }}'
                f'QToolButton#{self.name}:hover {{ background-color: {hover_background_color};'
                f'color: {hover_color} }}')

    def language_text(self, language):
        if language == 0:   self.setText(self.label_es)
        elif language == 1: self.setText(self.label_en)

# ----------------
# Segmented Button
# ----------------
class SegmentedButton(QtWidgets.QToolButton):
    def __init__(self, parent, name, geometry, labels, icons, position, state, theme, language):
        super(SegmentedButton, self).__init__(parent)

        self.name = name
        self.label_es, self.label_en = labels
        self.icon_on, self.icon_off = icons
        self.position = position
        x, y, w = geometry

        self.setObjectName(self.name)
        self.setGeometry(x, y, w, 32)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setCheckable(True)
        self.setEnabled(True)

        self.set_state(state)
        self.apply_styleSheet(theme)
        self.language_text(language)
        
    def set_state(self, state):
        if state:
            self.setIcon(QtGui.QIcon(f'{images_path}/{self.icon_on}'))
            self.setChecked(True)
        else:
            self.setIcon(QtGui.QIcon(f'{images_path}/{self.icon_off}'))
            self.setChecked(False)

    def apply_styleSheet(self, theme):
        if self.position == 'left':
            border_position = 'border-top-left-radius: 16; border-bottom-left-radius: 16'
        elif self.position == 'center':
            border_position = 'border-radius: 0'
        elif self.position == 'right':
            border_position = 'border-top-right-radius: 16; border-bottom-right-radius: 16'
        
        if theme:
            border_color = light["on_surface"]
            background_color = light["primary"]
            color = light["on_primary"]
            checked_background_color = light["secondary"]
            checked_color = light["on_secondary"]
        else:
            border_color = dark["on_surface"]
            background_color = dark["primary"]
            color = dark["on_primary"]
            checked_background_color = dark["secondary"]
            checked_color = dark["on_secondary"]
        self.setStyleSheet(f'QToolButton#{self.name} {{ border: 1px solid {border_color};'
                f'{border_position}; padding: 0 8 0 8;'
                f'background-color: {background_color}; color: {color} }}'
                f'QToolButton#{self.name}:checked {{ background-color: {checked_background_color};'
                f'color: {checked_color} }}')

    def language_text(self, language):
        if language == 0:   self.setText(self.label_es)
        elif language == 1: self.setText(self.label_en)
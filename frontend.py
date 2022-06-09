"""
Frontend

This file contains main UI class and methods to control components operations.
"""

from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QSettings

import sys
import pandas as pd
from pathlib import Path

import material3_components as mt3
import backend
import patient
import database


class App(QWidget):
    def __init__(self):
        """ UI main application """
        super().__init__()
        # --------
        # Settings
        # --------
        self.settings = QSettings(f'{sys.path[0]}/settings.ini', QSettings.Format.IniFormat)
        self.language_value = int(self.settings.value('language'))
        self.theme_value = eval(self.settings.value('theme'))

        self.idioma_dict = {0: ('ESP', 'SPA'), 1: ('ING', 'ENG')}

        # -------------
        # Base de Datos
        # -------------
        self.patientes_list = backend.create_db('pacientes')
        self.estudios_list = backend.create_db('estudios')

        # ---------
        # Variables
        # ---------
        self.patient_data = None
        self.data_lat_max = 0.0
        self.data_lat_t_max = 0.0
        self.data_lat_min = 0.0
        self.data_lat_t_min = 0.0
        self.data_ap_max = 0.0
        self.data_ap_t_max = 0.0
        self.data_ap_min = 0.0
        self.data_ap_t_min = 0.0
        self.lat_text_1 = None
        self.lat_text_2 = None
        self.ap_text_1 = None
        self.ap_text_2 = None

        # ----------------
        # Generación de UI
        # ----------------
        width = 1300
        height = 700
        screen_x = int(self.screen().availableGeometry().width() / 2 - (width / 2))
        screen_y = int(self.screen().availableGeometry().height() / 2 - (height / 2))

        if self.language_value == 0:
            self.setWindowTitle('Test de Romberg')
        elif self.language_value == 1:
            self.setWindowTitle("Romberg's Test")
        self.setGeometry(screen_x, screen_y, width, height)
        self.setMinimumSize(1300, 700)
        if self.theme_value:
            self.setStyleSheet(f'QWidget {{ background-color: #E5E9F0; color: #000000 }}'
                f'QComboBox QListView {{ border: 1px solid #000000; border-radius: 4;'
                f'background-color: #B2B2B2; color: #000000 }}')
        else:
            self.setStyleSheet(f'QWidget {{ background-color: #3B4253; color: #E5E9F0 }}'
                f'QComboBox QListView {{ border: 1px solid #E5E9F0; border-radius: 4;'
                f'background-color: #2E3441; color: #E5E9F0 }}')
        
        # -----------
        # Card Título
        # -----------
        self.titulo_card = mt3.Card(self, 'titulo_card',
            (8, 8, width-16, 48), ('',''), self.theme_value, self.language_value)


        # Espacio para título de la aplicación, logo, etc.

        
        self.idioma_menu = mt3.Menu(self.titulo_card, 'idioma_menu',
            (8, 8, 72), 2, 2, self.idioma_dict, self.theme_value, self.language_value)
        self.idioma_menu.setCurrentIndex(self.language_value)
        self.idioma_menu.currentIndexChanged.connect(self.on_idioma_menu_currentIndexChanged)
        
        self.tema_switch = mt3.Switch(self.titulo_card, 'tema_switch',
            (8, 8, 48), ('', ''), ('light_mode.png','dark_mode.png'), 
            self.theme_value, self.theme_value, self.language_value)
        self.tema_switch.clicked.connect(self.on_tema_switch_clicked)

        self.database_button = mt3.IconButton(self.titulo_card, 'database_button',
            (8, 8), 'database.png', self.theme_value)
        self.database_button.clicked.connect(self.on_database_button_clicked)

        self.manual_button = mt3.IconButton(self.titulo_card, 'manual_button',
            (8, 8), 'help.png', self.theme_value)
        self.manual_button.clicked.connect(self.on_manual_button_clicked)

        self.about_button = mt3.IconButton(self.titulo_card, 'about_button',
            (8, 8), 'mail_L.png', self.theme_value)
        self.about_button.clicked.connect(self.on_about_button_clicked)

        self.aboutQt_button = mt3.IconButton(self.titulo_card, 'aboutQt_button',
            (8, 8), 'about_qt.png', self.theme_value)
        self.aboutQt_button.clicked.connect(self.on_aboutQt_button_clicked)

        # -------------
        # Card Paciente
        # -------------
        self.paciente_card = mt3.Card(self, 'paciente_card',
            (8, 64, 180, 128), ('Paciente', 'Patient'), 
            self.theme_value, self.language_value)
        
        y_1 = 48
        self.pacientes_menu = mt3.Menu(self.paciente_card, 'pacientes_menu',
            (8, y_1, 164), 10, 10, {}, self.theme_value, self.language_value)
        for data in self.patientes_list:
            self.pacientes_menu.addItem(data[4])
        self.pacientes_menu.setCurrentIndex(-1)
        self.pacientes_menu.textActivated.connect(self.on_pacientes_menu_textActivated)

        y_1 += 40
        self.paciente_add_button = mt3.IconButton(self.paciente_card, 'paciente_add_button',
            (60, y_1), 'person_add.png', self.theme_value)
        self.paciente_add_button.clicked.connect(self.on_paciente_add_button_clicked)

        self.paciente_edit_button = mt3.IconButton(self.paciente_card, 'paciente_edit_button',
            (100, y_1), 'edit.png', self.theme_value)
        self.paciente_edit_button.clicked.connect(self.on_paciente_edit_button_clicked)

        self.paciente_del_button = mt3.IconButton(self.paciente_card, 'paciente_del_button',
            (140, y_1), 'person_off.png', self.theme_value)
        self.paciente_del_button.clicked.connect(self.on_paciente_del_button_clicked)

        # -------------
        # Card Análisis
        # -------------
        self.analisis_card = mt3.Card(self, 'analisis_card',
            (8, 200, 180, 128), ('Análsis', 'Analysis'), 
            self.theme_value, self.language_value)

        y_2 = 48
        self.analisis_menu = mt3.Menu(self.analisis_card, 'analisis_menu',
            (8, y_2, 164), 10, 10, {}, self.theme_value, self.language_value)
        self.analisis_menu.setEnabled(False)
        self.analisis_menu.textActivated.connect(self.on_analisis_menu_textActivated)

        y_2 += 40
        self.analisis_add_button = mt3.IconButton(self.analisis_card, 'analisis_add_button',
            (100, y_2), 'new.png', self.theme_value)
        self.analisis_add_button.setEnabled(False)
        self.analisis_add_button.clicked.connect(self.on_analisis_add_button_clicked)

        self.analisis_del_button = mt3.IconButton(self.analisis_card, 'analisis_del_button',
            (140, y_2), 'delete.png', self.theme_value)
        self.analisis_del_button.setEnabled(False)
        self.analisis_del_button.clicked.connect(self.on_analisis_del_button_clicked)

        # ----------------
        # Card Información
        # ----------------
        self.info_card = mt3.Card(self, 'info_card',
            (8, 336, 180, 312), ('Información', 'Information'), 
            self.theme_value, self.language_value)
        
        y_3 = 48
        self.apellido_value = mt3.ValueLabel(self.info_card, 'apellido_value',
            (8, y_3, 164), self.theme_value)

        y_3 += 32
        self.nombre_value = mt3.ValueLabel(self.info_card, 'nombre_value',
            (8, y_3, 164), self.theme_value)

        y_3 += 32
        self.id_label = mt3.IconLabel(self.info_card, 'id_label',
            (8, y_3), 'id', self.theme_value)

        self.id_value = mt3.ValueLabel(self.info_card, 'id_value',
            (48, y_3, 124), self.theme_value)

        y_3 += 32
        self.fecha_label = mt3.IconLabel(self.info_card, 'fecha_label',
            (8, y_3), 'calendar', self.theme_value)

        self.fecha_value = mt3.ValueLabel(self.info_card, 'fecha_value',
            (48, y_3, 124), self.theme_value)
        
        y_3 += 32
        self.sex_label = mt3.IconLabel(self.info_card, 'sex_label',
            (8, y_3), '', self.theme_value)

        self.sex_value = mt3.ValueLabel(self.info_card, 'sex_value',
            (48, y_3, 124), self.theme_value)

        y_3 += 32
        self.peso_label = mt3.IconLabel(self.info_card, 'peso_label',
            (8, y_3), 'weight', self.theme_value)

        self.peso_value = mt3.ValueLabel(self.info_card, 'peso_value',
            (48, y_3, 124), self.theme_value)

        y_3 += 32
        self.altura_label = mt3.IconLabel(self.info_card, 'altura_label',
            (8, y_3), 'height', self.theme_value)

        self.altura_value = mt3.ValueLabel(self.info_card, 'altura_value',
            (48, y_3, 124), self.theme_value)

        y_3 += 32
        self.bmi_value = mt3.ValueLabel(self.info_card, 'bmi_value',
            (48, y_3, 124), self.theme_value)
        
        # -----------------
        # Cards Main Window
        # -----------------
        self.lateral_plot_card = mt3.Card(self, 'lateral_plot_card',
            (188, 70, 900, 215), ('Oscilación Lateral','Lateral Oscillation'), 
            self.theme_value, self.language_value)
        self.lateral_plot = backend.MPLCanvas(self.lateral_plot_card, self.theme_value)
        
        self.antePost_plot_card = mt3.Card(self, 'antePost_plot_card',
            (188, 295, 900, 215), ('Oscilación Antero-Posterior','Antero-Posterior Oscillation'), 
            self.theme_value, self.language_value)
        self.antePost_plot = backend.MPLCanvas(self.antePost_plot_card, self.theme_value)

        self.elipse_plot_card = mt3.Card(self, 'elipse_plot_card',
            (188, 520, 300, 300), ('Elipse', 'Ellipse'), self.theme_value, self.language_value)
        self.elipse_plot = backend.MPLCanvas(self.elipse_plot_card, self.theme_value)

        self.hull_plot_card = mt3.Card(self, 'hull_plot_card',
            (520, 520, 300, 300), ('Envolvente', 'Hull'), self.theme_value, self.language_value)
        self.hull_plot = backend.MPLCanvas(self.hull_plot_card, self.theme_value)

        self.pca_plot_card = mt3.Card(self, 'pca_plot_card',
            (830, 520, 300, 300), ('Elipse Orientada', 'Oriented Ellipse'), self.theme_value, self.language_value)
        self.pca_plot = backend.MPLCanvas(self.pca_plot_card, self.theme_value)

        # ----------------------------------
        # Card Parámetros Oscilación Lateral
        # ----------------------------------
        self.lateral_card = mt3.Card(self, 'lateral_card',
            (8, 8, 208, 228), ('Lateral', 'Lateral'), 
            self.theme_value, self.language_value)

        y_4 = 48
        self.lat_rango_label = mt3.ItemLabel(self.lateral_card, 'lat_rango_label',
            (8, y_4), ('Rango (mm)', 'Range (mm)'), self.theme_value, self.language_value)
        y_4 += 20
        self.lat_rango_value = mt3.ValueLabel(self.lateral_card, 'lat_rango_value',
            (8, y_4, 192), self.theme_value)

        y_4 += 40
        self.lat_vel_label = mt3.ItemLabel(self.lateral_card, 'lat_vel_label',
            (8, y_4), ('Velocidad Media (mm/s)', 'Mean Velocity (mm/s)'), self.theme_value, self.language_value)
        y_4 += 20
        self.lat_vel_value = mt3.ValueLabel(self.lateral_card, 'lat_vel_value',
            (8, y_4, 192), self.theme_value)

        y_4 += 40
        self.lat_rms_label = mt3.ItemLabel(self.lateral_card, 'lat_rms_label',
            (8, y_4), ('RMS (mm)', 'RMS (mm)'), self.theme_value, self.language_value)
        y_4 += 20
        self.lat_rms_value = mt3.ValueLabel(self.lateral_card, 'lat_rms_value',
            (8, y_4, 192), self.theme_value)

        # -------------------------------------------
        # Card Parámetros Oscilación Antero-Posterior
        # -------------------------------------------
        self.antPost_card = mt3.Card(self, 'antPost_card',
            (8, 8, 208, 228), ('Antero-Posterior', 'Antero-Posterior'), 
            self.theme_value, self.language_value)

        y_5 = 48
        self.ap_rango_label = mt3.ItemLabel(self.antPost_card, 'ap_rango_label',
            (8, y_5), ('Rango (mm)', 'Range (mm)'), self.theme_value, self.language_value)
        y_5 += 20
        self.ap_rango_value = mt3.ValueLabel(self.antPost_card, 'ap_rango_value',
            (8, y_5, 192), self.theme_value)

        y_5 += 40
        self.ap_vel_label = mt3.ItemLabel(self.antPost_card, 'ap_vel_label',
            (8, y_5), ('Velocidad Media (mm/s)', 'Mean Velocity (mm/s)'), self.theme_value, self.language_value)
        y_5 += 20
        self.ap_vel_value = mt3.ValueLabel(self.antPost_card, 'ap_vel_value',
            (8, y_5, 192), self.theme_value)

        y_5 += 40
        self.ap_rms_label = mt3.ItemLabel(self.antPost_card, 'ap_rms_label',
            (8, y_5), ('RMS (mm)', 'RMS (mm)'), self.theme_value, self.language_value)
        y_5 += 20
        self.ap_rms_value = mt3.ValueLabel(self.antPost_card, 'ap_rms_value',
            (8, y_5, 192), self.theme_value)

        # ----------------------
        # Card Centro de Presión
        # ----------------------
        self.centro_card = mt3.Card(self, 'centro_card',
            (8, 8, 208, 228), ('Centro de Presión', 'Center of Pressure'), 
            self.theme_value, self.language_value)

        y_6 = 48
        self.cop_vel_label = mt3.ItemLabel(self.centro_card, 'cop_vel_label',
            (8, y_6), ('Velocidad Media (mm/s)', 'Mean Velocity (mm/s)'), self.theme_value, self.language_value)
        y_6 += 20
        self.cop_vel_value = mt3.ValueLabel(self.centro_card, 'cop_vel_value',
            (8, y_6, 192), self.theme_value)

        y_6 += 40
        self.distancia_label = mt3.ItemLabel(self.centro_card, 'distancia_label',
            (8, y_6), ('Distancia Media (mm)', 'Mean Distance (mm)'), self.theme_value, self.language_value)
        y_6 += 20
        self.distancia_value = mt3.ValueLabel(self.centro_card, 'distancia_value',
            (8, y_6, 192), self.theme_value)

        y_6 += 40
        self.frecuencia_label = mt3.ItemLabel(self.centro_card, 'frecuencia_label',
            (8, y_6), ('Frecuencia Media (Hz)', 'Mean Frequency (Hz)'), self.theme_value, self.language_value)
        y_6 += 20
        self.frecuencia_value = mt3.ValueLabel(self.centro_card, 'frecuencia_value',
            (8, y_6, 192), self.theme_value)

        # ----------
        # Card Áreas
        # ----------
        self.areas_card = mt3.Card(self, 'areas_card',
            (8, 8, 208, 228), ('Áreas', 'Areas'), 
            self.theme_value, self.language_value)

        y_7 = 48
        self.elipse_label = mt3.ItemLabel(self.areas_card, 'elipse_label',
            (8, y_7), ('Área de la Elipse (mm²)', 'Ellipse Area (mm²)'), self.theme_value, self.language_value)
        y_7 += 20
        self.elipse_value = mt3.ValueLabel(self.areas_card, 'elipse_value',
            (8, y_7, 192), self.theme_value)

        y_7 += 40
        self.hull_label = mt3.ItemLabel(self.areas_card, 'hull_label',
            (8, y_7), ('Área del Envolvente (mm²)', 'Hull Area (mm²)'), self.theme_value, self.language_value)
        y_7 += 20
        self.hull_value = mt3.ValueLabel(self.areas_card, 'hull_value',
            (8, y_7, 192), self.theme_value)
        
        y_7 += 40
        self.pca_label = mt3.ItemLabel(self.areas_card, 'pca_label',
            (8, y_7), ('Área de la Elipse Orientada (mm²)', 'Oriented Ellipse Area (mm²)'), self.theme_value, self.language_value)
        y_7 += 20
        self.pca_value = mt3.ValueLabel(self.areas_card, 'pca_value',
            (8, y_7, 192), self.theme_value)

# ----------------
    # Funciones Título
    # ----------------
    def on_idioma_menu_currentIndexChanged(self, index: int) -> None:
        """ Language menu control to change components text language
        
        Parameters
        ----------
        index: int
            Index of language menu control
        
        Returns
        -------
        None
        """
        self.idioma_menu.language_text(index)
        
        self.paciente_card.language_text(index)
        self.analisis_card.language_text(index)
        self.info_card.language_text(index)

        self.lateral_plot_card.language_text(index)
        self.antePost_plot_card.language_text(index)
        self.elipse_plot_card.language_text(index)
        self.hull_plot_card.language_text(index)
        self.pca_plot_card.language_text(index)

        self.lateral_card.language_text(index)
        self.lat_rango_label.language_text(index)
        self.lat_vel_label.language_text(index)
        self.lat_rms_label.language_text(index)

        self.antPost_card.language_text(index)
        self.ap_rango_label.language_text(index)
        self.ap_vel_label.language_text(index)
        self.ap_rms_label.language_text(index)
        
        self.centro_card.language_text(index)
        self.cop_vel_label.language_text(index)
        self.distancia_label.language_text(index)
        self.frecuencia_label.language_text(index)

        self.areas_card.language_text(index)
        self.elipse_label.language_text(index)
        self.hull_label.language_text(index)
        self.pca_label.language_text(index)

        self.settings.setValue('language', str(index))
        self.language_value = int(self.settings.value('language'))


    def on_tema_switch_clicked(self, state: bool) -> None:
        """ Theme switch control to change components stylesheet
        
        Parameters
        ----------
        state: bool
            State of theme switch control
        
        Returns
        -------
        None
        """
        if state: self.setStyleSheet('background-color: #E5E9F0; color: #000000')
        else: self.setStyleSheet('background-color: #3B4253; color: #E5E9F0')

        self.titulo_card.apply_styleSheet(state)
        self.idioma_menu.apply_styleSheet(state)
        self.tema_switch.set_state(state)
        self.tema_switch.apply_styleSheet(state)
        self.database_button.apply_styleSheet(state)
        self.manual_button.apply_styleSheet(state)
        self.about_button.apply_styleSheet(state)
        self.aboutQt_button.apply_styleSheet(state)

        self.paciente_card.apply_styleSheet(state)
        self.paciente_add_button.apply_styleSheet(state)
        self.paciente_edit_button.apply_styleSheet(state)
        self.paciente_del_button.apply_styleSheet(state)
        self.pacientes_menu.apply_styleSheet(state)

        self.analisis_card.apply_styleSheet(state)
        self.analisis_add_button.apply_styleSheet(state)
        self.analisis_del_button.apply_styleSheet(state)
        self.analisis_menu.apply_styleSheet(state)

        self.info_card.apply_styleSheet(state)
        self.apellido_value.apply_styleSheet(state)
        self.nombre_value.apply_styleSheet(state)
        self.id_label.apply_styleSheet(state)
        self.id_label.set_icon('id', state)
        self.id_value.apply_styleSheet(state)
        self.fecha_label.apply_styleSheet(state)
        self.fecha_label.set_icon('calendar', state)
        self.fecha_value.apply_styleSheet(state)
        self.sex_label.apply_styleSheet(state)
        self.sex_value.apply_styleSheet(state)
        
        if self.sex_value.text() == 'F': self.sex_label.set_icon('woman', state)
        elif self.sex_value.text() == 'M': self.sex_label.set_icon('man', state)

        self.peso_label.apply_styleSheet(state)
        self.peso_label.set_icon('weight', state)
        self.peso_value.apply_styleSheet(state)
        self.altura_label.apply_styleSheet(state)
        self.altura_label.set_icon('height', state)
        self.altura_value.apply_styleSheet(state)
        self.bmi_value.apply_styleSheet(state)

        self.lateral_plot_card.apply_styleSheet(state)
        self.antePost_plot_card.apply_styleSheet(state)
        self.elipse_plot_card.apply_styleSheet(state)
        self.hull_plot_card.apply_styleSheet(state)
        self.pca_plot_card.apply_styleSheet(state)

        self.lateral_plot.apply_styleSheet(state)
        if self.lat_text_1:
            self.lat_text_1.remove()
            self.lat_text_2.remove()
            if state:
                self.lat_text_1 = self.lateral_plot.axes.text(self.data_lat_t_max, self.data_lat_max, f'{self.data_lat_max:.2f}', color='#000000')
                self.lat_text_2 = self.lateral_plot.axes.text(self.data_lat_t_min, self.data_lat_min, f'{self.data_lat_min:.2f}', color='#000000')
            else:
                self.lat_text_1 = self.lateral_plot.axes.text(self.data_lat_t_max, self.data_lat_max, f'{self.data_lat_max:.2f}', color='#E5E9F0')
                self.lat_text_2 = self.lateral_plot.axes.text(self.data_lat_t_min, self.data_lat_min, f'{self.data_lat_min:.2f}', color='#E5E9F0')
        self.lateral_plot.draw()
        self.antePost_plot.apply_styleSheet(state)
        if self.ap_text_1:
            self.ap_text_1.remove()
            self.ap_text_2.remove()
            if state:
                self.ap_text_1 = self.antePost_plot.axes.text(self.data_ap_t_max, self.data_ap_max, f'{self.data_ap_max:.2f}', color='#000000')
                self.ap_text_2 = self.antePost_plot.axes.text(self.data_ap_t_min, self.data_ap_min, f'{self.data_ap_min:.2f}', color='#000000')
            else:
                self.ap_text_1 = self.antePost_plot.axes.text(self.data_ap_t_max, self.data_ap_max, f'{self.data_ap_max:.2f}', color='#E5E9F0')
                self.ap_text_2 = self.antePost_plot.axes.text(self.data_ap_t_min, self.data_ap_min, f'{self.data_ap_min:.2f}', color='#E5E9F0')
        self.antePost_plot.draw()
        self.elipse_plot.apply_styleSheet(state)
        self.elipse_plot.draw()
        self.hull_plot.apply_styleSheet(state)
        self.hull_plot.draw()
        self.pca_plot.apply_styleSheet(state)
        self.pca_plot.draw()

        self.lateral_card.apply_styleSheet(state)
        self.lat_rango_label.apply_styleSheet(state)
        self.lat_rango_value.apply_styleSheet(state)
        self.lat_vel_label.apply_styleSheet(state)
        self.lat_vel_value.apply_styleSheet(state)
        self.lat_rms_label.apply_styleSheet(state)
        self.lat_rms_value.apply_styleSheet(state)

        self.antPost_card.apply_styleSheet(state)
        self.ap_rango_label.apply_styleSheet(state)
        self.ap_rango_value.apply_styleSheet(state)
        self.ap_vel_label.apply_styleSheet(state)
        self.ap_vel_value.apply_styleSheet(state)
        self.ap_rms_label.apply_styleSheet(state)
        self.ap_rms_value.apply_styleSheet(state)

        self.centro_card.apply_styleSheet(state)
        self.cop_vel_label.apply_styleSheet(state)
        self.cop_vel_value.apply_styleSheet(state)
        self.distancia_label.apply_styleSheet(state)
        self.distancia_value.apply_styleSheet(state)
        self.frecuencia_label.apply_styleSheet(state)
        self.frecuencia_value.apply_styleSheet(state)

        self.areas_card.apply_styleSheet(state)
        self.elipse_label.apply_styleSheet(state)
        self.elipse_value.apply_styleSheet(state)
        self.hull_label.apply_styleSheet(state)
        self.hull_value.apply_styleSheet(state)
        self.pca_label.apply_styleSheet(state)
        self.pca_value.apply_styleSheet(state)

        self.settings.setValue('theme', f'{state}')
        self.theme_value = eval(self.settings.value('theme'))


    def on_database_button_clicked(self) -> None:
        """ Database button to configure the database """
        self.db_info = database.Database()
        self.db_info.exec()

        if self.db_info.database_data:
            if self.language_value == 0:
                QtWidgets.QMessageBox.information(self, 'Datos Guardados', 'Base de datos configurada')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.information(self, 'Data Saved', 'Database configured')
        else:
            if self.language_value == 0:
                QtWidgets.QMessageBox.critical(self, 'Error de Datos', 'No se dio información de la base de datos')
            elif self.language_value == 1:
                QtWidgets.QMessageBox.critical(self, 'Data Error', 'No information on the database was given')


    def on_manual_button_clicked(self) -> None:
        """ Manual button to open manual window """
        return 0


    def on_about_button_clicked(self) -> None:
        """ About app button to open about app window dialog """
        self.about = backend.AboutApp()
        self.about.exec()


    def on_aboutQt_button_clicked(self) -> None:
        """ About Qt button to open about Qt window dialog """
        backend.about_qt_dialog(self, self.language_value)
        
    
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """ Resize event to control size and position of app components """
        width = self.geometry().width()
        height = self.geometry().height()

        self.titulo_card.resize(width - 16, 48)
        self.titulo_card.title.resize(width - 304, 32)
        self.idioma_menu.move(width - 312, 8)
        self.tema_switch.move(width - 232, 8)
        self.database_button.move(width - 176, 8)
        self.manual_button.move(width - 136, 8)
        self.about_button.move(width - 96, 8)
        self.aboutQt_button.move(width - 56, 8)

        self.lateral_plot_card.setGeometry(196, 64, width - 636, int(height * 0.25))
        self.lateral_plot_card.title.resize(width - 652, 32)
        self.lateral_plot.setGeometry(8, 48, self.lateral_plot_card.width()-16, self.lateral_plot_card.height()-56)
        
        self.antePost_plot_card.setGeometry(196, int(72 + (height * 0.25)), width - 636, int(height * 0.25))
        self.antePost_plot_card.title.resize(width - 652, 32)
        self.antePost_plot.setGeometry(8, 48, self.antePost_plot_card.width()-16, self.antePost_plot_card.height()-56)
        
        self.elipse_plot_card.setGeometry(196, int(80 + (height * 0.5)), int((width - 652) / 3), int(height - (88 + (height * 0.5))))
        self.elipse_plot_card.title.resize(self.elipse_plot_card.width() - 16, 32)
        self.elipse_plot.setGeometry(8, 48, self.elipse_plot_card.width()-16, self.elipse_plot_card.height()-56)
        
        self.hull_plot_card.setGeometry(int(204 + ((width - 652) / 3)), int(80 + (height * 0.5)), int((width - 652) / 3), int(height - (88 + (height * 0.5))))
        self.hull_plot_card.title.resize(self.hull_plot_card.width() - 16, 32)
        self.hull_plot.setGeometry(8, 48, self.hull_plot_card.width()-16, self.hull_plot_card.height() - 56)
        
        self.pca_plot_card.setGeometry(int(212 + (2 * (width - 652) / 3)), int(80 + (height * 0.5)), int((width - 652) / 3), int(height - (88 + (height * 0.5))))
        self.pca_plot_card.title.resize(self.pca_plot_card.width() - 16, 32)
        self.pca_plot.setGeometry(8, 48, self.pca_plot_card.width()-16, self.pca_plot_card.height() - 56)
        
        self.lateral_card.setGeometry(width - 432, 64, 208, 228)
        self.antPost_card.setGeometry(width - 216, 64, 208, 228)
        self.centro_card.setGeometry(width - 432, 300, 208, 228)
        self.areas_card.setGeometry(width - 216, 300, 208, 228)

        return super().resizeEvent(a0)


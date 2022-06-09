"""
Backend

This file contains supplementary methods and classes applied to the frontend.

1. Class MPLCanvas: configuration of the plot canvas
2. Analysis methods: methods to process and analyze balance signals data
3. Database methods: methods of the database operations
4. About class and method: Dialogs of information about me and Qt

"""

from PyQt6 import QtWidgets
from PyQt6.QtCore import QSettings

import sys
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
import psycopg2

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import material3_components as mt3

light = {
    'surface': '#B2B2B2',
    'on_surface': '#000000'
}

dark = {
    'surface': '#2E3441',
    'on_surface': '#E5E9F0'
}

class MPLCanvas(FigureCanvasQTAgg):
    def __init__(self, parent, theme: bool) -> None:
        """ Canvas settings for plotting signals """
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        self.apply_styleSheet(theme)

    def apply_styleSheet(self, theme):
        self.fig.subplots_adjust(left=0.05, bottom=0.15, right=1, top=0.95, wspace=0, hspace=0)
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['bottom'].set_visible(False)
        self.axes.spines['left'].set_visible(False)
        if theme:
            self.fig.set_facecolor(f'{light["surface"]}')
            self.axes.set_facecolor(f'{light["surface"]}')
            self.axes.xaxis.label.set_color(f'{light["on_surface"]}')
            self.axes.yaxis.label.set_color(f'{light["on_surface"]}')
            self.axes.tick_params(axis='both', colors=f'{light["on_surface"]}', labelsize=8)
        else:
            self.fig.set_facecolor(f'{dark["surface"]}')
            self.axes.set_facecolor(f'{dark["surface"]}')
            self.axes.xaxis.label.set_color(f'{dark["on_surface"]}')
            self.axes.yaxis.label.set_color(f'{dark["on_surface"]}')
            self.axes.tick_params(axis='both', colors=f'{dark["on_surface"]}', labelsize=8)


def analisis(df: pd.DataFrame) -> dict:
    """ Analysis of dataframe from balance signal

    Parameters
    ----------
    df: pd.DataFrame
        Pandas dataframe converted from balance signal data from file
    
    Returns
    -------
    results: dict
        Results of dataframe analysis of lateral, antero-posterior, and
        center of pressure oscillations
        data_x: pd.DataFrame
            Lateral signal
        data_y: pd.DataFrame
            Antero-posterior signal
        data_t: 
            Time signal
        lat_max: float
            Lateral signal maximum value
        lat_t_max: float
            Lateral signal correspondent time value for maximum value
        lat_min: float
            Lateral signal minimum value
        lat_t_min: float
            Lateral signal correspondent time value for minimum value
        ap_max: float
            Antero-posterior signal maximum value
        ap_t_max: float
            Antero-posterior signal correspondent time value for maximum value
        ap_min: float
            Antero-posterior signal minimum value
        ap_t_min: float
            Antero-posterior signal correspondent time value for minimum value
        lat_rango: float
            Lateral signal range
        ap_rango: float
            Antero-posterior signal range
        lat_vel: float
            Lateral signal mean velocity
        lat_rms: float
            Lateral signal RMS
        ap_vel: float
            Antero-posterior signal mean velocity
        ap_rms: float
            Antero-posterior signal RMS
        centro_vel: float
            Center of pressure signal mean velocity
        centro_dist: float
            Center of pressure signal mean distance
        centro_frec: float
            Center of pressure signal mean frequency
    """
    results = {}

    data_x = df.iloc[:,0]
    data_y = df.iloc[:,1]
    data_t = np.linspace(0, len(df) / 10, len(df))

    results['data_x'] = data_x
    results['data_y'] = data_y
    results['data_t'] = data_t

    x_max = data_x.max()
    x_min = data_x.min()
    y_max = data_y.max()
    y_min = data_y.min()

    results['lat_max'] = x_max
    results['lat_t_max'] = data_x.idxmax() / 10
    results['lat_min'] = x_min
    results['lat_t_min'] = data_x.idxmin() / 10

    results['ap_max'] = y_max
    results['ap_t_max'] = data_y.idxmax() / 10
    results['ap_min'] = y_min
    results['ap_t_min'] = data_y.idxmin() / 10

    results['lat_rango'] = x_max - x_min
    results['ap_rango'] = y_max - y_min

    tAnalisis = len(df) / 10
    time_analysis = len(df) - 1
    den = tAnalisis / len(df)

    # SEÑAL X ----------------------------------------------------------------
    avgX = data_x.sum() / len(df)

    numX = abs(data_x.diff()).dropna()
    velSgnX = numX / den
    results['lat_vel'] = velSgnX.sum() / time_analysis

    numRMSX = (data_x - avgX) * (data_x - avgX)
    results['lat_rms'] = np.sqrt(numRMSX.sum() / time_analysis)
    
    # SEÑAL Y ----------------------------------------------------------------
    avgY = data_y.sum() / len(df)

    numY = abs(data_y.diff()).dropna()
    velSgnY = numY / den
    results['ap_vel'] = velSgnY.sum() / time_analysis

    numRMSY = (data_y - avgY) * (data_y - avgY)
    results['ap_rms'] = np.sqrt(numRMSY.sum() / time_analysis)

    # SEÑALES X Y ------------------------------------------------------------
    num2 = np.sqrt((numX * numX) + (numY * numY))
    numVMT = num2 / tAnalisis
    results['centro_vel'] = numVMT.sum()

    numDist = np.sqrt((data_x * data_x) + (data_y * data_y))
    distM = numDist / tAnalisis

    results['centro_dist'] = distM.sum()
    results['centro_frec'] = numVMT.sum() / (2 * np.pi)

    return results


# ------
# Elipse
# ------
def ellipseStandard(df: pd.DataFrame) -> dict:
    """ Ellipse analysis of dataframe from balance signal

    Parameters
    ----------
    df: pd.DataFrame
        Pandas dataframe converted from balance signal data from file
    
    Returns
    -------
    results: dict
        Results of ellipse clustering analysis
        x: list
            x-coordinates of ellipse points
        y: list
            y-coordinates of ellipse points
        area: float
            area of ellipse
    """
    data_x = df.iloc[:,0]
    data_y = df.iloc[:,1]

    x_max = data_x.max()
    x_min = data_x.min()
    y_max = data_y.max()
    y_min = data_y.min()

    a = (x_max - x_min) / 2
    b = (y_max - y_min) / 2
    x0 = x_max - a
    y0 = y_max - b

    theta = np.linspace(0, 2 * np.pi, 100)
    x = x0 + a * np.cos(theta)
    y = y0 + b * np.sin(theta)

    results = {
        'x': x,
        'y': y,
        'area': np.pi * a * b
    }

    return results


# -----------
# Convex Hull
# -----------
def convexHull(df: pd.DataFrame) -> dict:
    """ Convex hull analysis of dataframe from balance signal

    Parameters
    ----------
    df: pd.DataFrame
        Pandas dataframe converted from balance signal data from file
    
    Returns
    -------
    results: dict
        Results of convex hull clustering analysis
        x: list
            x-coordinates of convex hull points
        y: list
            y-coordinates of convex hull points
        area: float
            area of convex hull
    """
    data_x = df.iloc[:,0]
    data_y = df.iloc[:,1]
    data = np.stack((data_x.to_numpy(), data_y.to_numpy()), axis=1)

    hull = ConvexHull(data)
    hullX = data[hull.vertices, 0]
    hullY = data[hull.vertices, 1]

    results = {
        'x': hullX,
        'y': hullY,
        'area': hull.volume # 2D Area
    }

    return results


# ----------------
# Elipse Orientada
# ----------------
def ellipsePCA(df: pd.DataFrame) -> dict:
    """ Oriented ellipse analysis of dataframe from balance signal

    Parameters
    ----------
    df: pd.DataFrame
        Pandas dataframe converted from balance signal data from file
    
    Returns
    -------
    results: dict
        Results of oriented ellipse clustering analysis
        x: list
            x-coordinates of oriented ellipse points
        y: list
            y-coordinates of oriented ellipse points
        area: float
            area of oriented ellipse
    """
    data_x = df.iloc[:,0]
    data_y = df.iloc[:,1]

    sumX = data_x.sum()
    sumY = data_y.sum()
    cen = ( sumX / len(df) , sumY / len(df) )

    covXX = (data_x - cen[0]) * (data_x - cen[0])
    covXY = (data_x - cen[0]) * (data_y - cen[1])
    covYY = (data_y - cen[1]) * (data_y - cen[1])
    JX = data_x - cen[0]
    JY = data_y - cen[1]
    theta = np.arctan2(JY , JX)
    rho = np.sqrt((JX * JX) + (JY * JY))

    a = covXX.sum() / len(covXX)
    b = covXY.sum() / len(covXY)
    d = covYY.sum() / len(covYY)

    B = a + d
    C = a * d - b * b
    L1 = (B / 2) + np.sqrt(B * B - 4 * C) / 2
    eigvec = ( L1 - d , b )

    rot = np.arctan( (L1 - d) / b )

    thetarot = theta + rot
    rotX = rho * np.cos(thetarot)
    rotY = rho * np.sin(thetarot)

    maxX = rotX.max()
    minX = rotX.min()
    maxY = rotY.max()
    minY = rotY.min()

    aa = (maxX - minX) / 2
    bb = (maxY - minY) / 2
    x0 = maxX - aa
    y0 = maxY - bb

    phi = np.linspace(0, 2 * np.pi, 100)
    newX = x0 + aa * np.cos(phi)
    newY = y0 + bb * np.sin(phi)
    thetaellipse = np.arctan2(newY, newX)
    rhoellipse = np.sqrt((newX * newX) + (newY * newY))
    thetarotellipse = thetaellipse - rot
    Xellipse = rhoellipse * np.cos(thetarotellipse)
    Yellipse = rhoellipse * np.sin(thetarotellipse)
    XellipseFinal = Xellipse + cen[0]
    YellipseFinal = Yellipse + cen[1]

    results = {
        'x': XellipseFinal,
        'y': YellipseFinal,
        'area': np.pi * aa * bb
    }

    return results
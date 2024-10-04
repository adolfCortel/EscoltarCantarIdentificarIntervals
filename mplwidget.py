# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------

# s'ha afegit  la navigation tool bar

from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure


class MplWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())  # FigureCanvas es una classe de  matplotlib definida per compatibilitat
                                            # amb QtDesigner

        vertical_layout = QVBoxLayout()
        """
        self.navi_toolbar = NavigationToolbar(self.canvas, self) #createa navigation toolbar for our plot canvas
        # s'afegeix primer la barra de navegacio per que quedia dal
        vertical_layout.addWidget(self.navi_toolbar)
        """
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_axes([0.01,0.01,0.95,0.95]) # Add an Axes to the figure as part of a subplot arrangement.

        self.canvas.axes.set_axis_off()
        self.setLayout(vertical_layout)

"""Cellular Automata Sandbox
    Simulations:
        Conway's Game of Life
        Langton's Ant
        Wireworld
    Add new widgets by importing them and registering them in SIMULATIONS
"""

import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QLabel, QSlider, QAction, QStyle
)

# Import all simulation widgets
from game_of_life import GameOfLifeWidget
from langton_ant import LangtonsAntWidget
from wireworld import WireworldWidget

# simulations dictionary
SIMULATIONS = {}
SIMULATIONS["Conway's Game of Life"] = GameOfLifeWidget
SIMULATIONS["Langton's Ant"] = LangtonsAntWidget
SIMULATIONS["Wireworld"] = WireworldWidget


class ClickJumpSlider(QSlider):
    """A slider whose handle jumps to the point you click"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.orientation() == Qt.Horizontal:
                val = QStyle.sliderValueFromPosition(
                    self.minimum(), self.maximum(), event.x(), self.width()
                )
            else:      # vertical slider
                val = QStyle.sliderValueFromPosition(
                    self.minimum(), self.maximum(), event.y(),
                    self.height(), upsideDown=True
                )
            self.setValue(val)
            event.accept()
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    """Main window with selectable simulator canvas"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cellular Automata Sandbox")

        #   Static controls
        self.start_button = QPushButton("Start")
        self.stop_button  = QPushButton("Stop")
        self.clear_button = QPushButton("Clear")

        self.speed_slider = ClickJumpSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 200)
        self.speed_slider.setValue(30)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(0)

        self._build_layout()
        self._build_menu()
        self._init_timer()

        default_sim = next(iter(SIMULATIONS)) if SIMULATIONS else None
        if default_sim:
            self._switch_simulation(default_sim)
        else:
            self.setCentralWidget(QLabel("No simulation widgets found."))

    # layout and menu setup
    def _build_layout(self):
        speed_label = QLabel("Speed (steps/sec)")

        button_row = QHBoxLayout()
        button_row.addWidget(self.start_button)
        button_row.addWidget(self.stop_button)
        button_row.addWidget(self.clear_button)

        slider_row = QHBoxLayout()
        slider_row.addWidget(speed_label)
        slider_row.addWidget(self.speed_slider)

        self.main_layout = QVBoxLayout()   
        self.main_layout.addLayout(button_row)
        self.main_layout.addLayout(slider_row)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)
        self.clear_button.setEnabled(False)   
        self.speed_slider.valueChanged.connect(self._update_timer_interval)

    def _build_menu(self):
        sim_menu = self.menuBar().addMenu("Simulation")
        for name in SIMULATIONS:
            act = QAction(name, self)
            act.triggered.connect(lambda _, n=name: self._switch_simulation(n))
            sim_menu.addAction(act)

    def _init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: None)  
        self._update_timer_interval()


    # switching simulations

    def _switch_simulation(self, name: str):
        """Switch to the specified simulation widget by name"""
        self.stop()                          # stop any running timer

        if hasattr(self, "game_widget"):
            self.main_layout.removeWidget(self.game_widget)
            self.game_widget.deleteLater()

        widget_cls = SIMULATIONS[name]
        self.game_widget = widget_cls()
        self.main_layout.insertWidget(0, self.game_widget, alignment=Qt.AlignCenter)

        # reconnect dynamic signals
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.game_widget.step)

        try:
            self.clear_button.clicked.disconnect()
        except TypeError:
            pass
        self.clear_button.clicked.connect(self.game_widget.clear)
        self.clear_button.setEnabled(True)

        self.setWindowTitle(f"Cellular Automata Sandbox -- {name}")


    def start(self):
        self.timer.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def _update_timer_interval(self):
        self.timer.setInterval(int(100 / self.speed_slider.value()))


# Keep app & window global so they don’t get garbage-collected.
app: QApplication | None = None
window: MainWindow | None = None


def main() -> None:
    global app, window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())   


if __name__ == "__main__":
    main()

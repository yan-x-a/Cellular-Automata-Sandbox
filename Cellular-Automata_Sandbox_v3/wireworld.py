"""
4 states
  0  EMPTY           - black
  1  ELECTRON_HEAD   - blue
  2  ELECTRON_TAIL   - red
  3  WIRE            - yellow

Transition rules (applied simultaneously to all cells each step):
  EMPTY           → EMPTY
  ELECTRON_HEAD   → ELECTRON_TAIL
  ELECTRON_TAIL   → WIRE
  WIRE            → ELECTRON_HEAD if 1 or 2 neighboring heads, else WIRE
"""
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from base_widget import BaseAutomatonWidget

CELL_SIZE    = 20
EMPTY_COLOR  = QColor(0, 0, 0)
HEAD_COLOR   = QColor( 50, 130, 255)   # blue
TAIL_COLOR   = QColor(220, 40, 40)     # red
WIRE_COLOR   = QColor(220, 220,  40)   # yellow
GRID_COLOR   = QColor(60, 60, 60)

STATE_COLORS = [EMPTY_COLOR, HEAD_COLOR, TAIL_COLOR, WIRE_COLOR]


class WireworldWidget(BaseAutomatonWidget):
    """Wireworld widget"""
    def __init__(self, rows: int = 120, cols: int = 190, cell_size: int = 10, parent=None):
        super().__init__(rows, cols, cell_size = 10, background_color=EMPTY_COLOR, parent=parent)

        self.drawing       = False
        self.draw_state    = 3       
        self.erase_mode    = False


    # rendering
    def paintEvent(self, event):
        painter = QPainter(self)
        # fill entire board as EMPTY first
        painter.fillRect(self.rect(), EMPTY_COLOR)

        # draw cells
        for y in range(self.rows):
            for x in range(self.cols):
                state = self.grid[y][x]
                if state:  # skip EMPTY to save a fillRect
                    painter.fillRect(
                        x * CELL_SIZE, y * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE,
                        STATE_COLORS[state]
                    )

        # draw grid lines
        painter.setPen(QPen(GRID_COLOR))
        for x in range(self.cols + 1):
            painter.drawLine(x * CELL_SIZE, 0,
                             x * CELL_SIZE, self.rows * CELL_SIZE)
        for y in range(self.rows + 1):
            painter.drawLine(0, y * CELL_SIZE,
                             self.cols * CELL_SIZE, y * CELL_SIZE)

    # interaction
    def _cell_at(self, event):
        return event.x() // CELL_SIZE, event.y() // CELL_SIZE

    def mousePressEvent(self, event):
        x, y = self._cell_at(event)
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.drawing = True
            if event.button() == Qt.RightButton:
                self.erase_mode = True
                self.set_cell(x, y, 0)          # erase to EMPTY
            else:  
                self.erase_mode = False
                # cycle through states 
                new_state = (self.grid[y][x] + 3) % 4  # skip 2-step to keep order
                self.draw_state = new_state
                self.set_cell(x, y, new_state)

    def mouseMoveEvent(self, event):
        if not self.drawing:
            return
        x, y = self._cell_at(event)
        if self.erase_mode:
            self.set_cell(x, y, 0)
        else:
            self.set_cell(x, y, self.draw_state)

    def mouseReleaseEvent(self, event):
        self.drawing = False

    def set_cell(self, x, y, state):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            if self.grid[y][x] != state:
                self.grid[y][x] = state
                self.update()

    # simulation
    def step(self):
        new_grid = [[0] * self.cols for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                state = self.grid[y][x]

                # Empty stays empty
                if state == 0:
                    new_grid[y][x] = 0
                    continue

                # Electron head → tail
                if state == 1:
                    new_grid[y][x] = 2
                    continue

                # Electron tail → wire
                if state == 2:
                    new_grid[y][x] = 3
                    continue

                # Wire: count neighboring heads
                if state == 3:
                    heads = 0
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            if self.grid[(y + dy) % self.rows][(x + dx) % self.cols] == 1:
                                heads += 1
                    new_grid[y][x] = 1 if heads in (1, 2) else 3

        self.grid = new_grid
        self.update()

    def clear(self):
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.update()

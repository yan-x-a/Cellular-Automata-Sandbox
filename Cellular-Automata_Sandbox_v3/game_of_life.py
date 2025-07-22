from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

from base_widget import BaseAutomatonWidget


ALIVE_COLOR = QColor(40, 40, 40)
DEAD_COLOR  = QColor(240, 240, 240)
GRID_COLOR  = QColor(200, 200, 200)


class GameOfLifeWidget(BaseAutomatonWidget):
    """
    Conway's Game of Life widget.
    This widget implements the rules of Conway's Game of Life.
    """

    def __init__(self, rows: int = 120, cols: int = 190, cell_size: int = 10, parent=None):
        super().__init__(rows, cols, cell_size = 10, background_color=DEAD_COLOR, parent=parent)

    # rendering
    def paintEvent(self, event):
        painter = QPainter(self)
        self.fill_background(painter)  # Fill background with DEAD_COLOR

        # Live cells
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x]:
                    painter.fillRect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                        ALIVE_COLOR,
                    )

        # Optional grid overlay
        painter.setPen(QPen(GRID_COLOR))
        self.draw_grid_lines(painter)

    # interaction
    def mousePressEvent(self, event):
        x, y = self.cell_at_event(event)
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.drawing = True
            self.draw_state = 0 if self.grid[y][x] == 1 else 1
            self.set_cell(x, y, self.draw_state)

    def mouseMoveEvent(self, event):
        if self.drawing and event.buttons() & Qt.LeftButton:
            x, y = self.cell_at_event(event)
            self.set_cell(x, y, self.draw_state)

    def mouseReleaseEvent(self, event):
        self.drawing = False

    def set_cell(self, x: int, y: int, state: int):
        if 0 <= x < self.cols and 0 <= y < self.rows and self.grid[y][x] != state:
            self.grid[y][x] = state
            self.update()

    # simulation
    def step(self):
        """Apply Conway’s rules and repaint."""
        new_grid = [[0] * self.cols for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                alive_neighbors = sum(
                    self.grid[(y + dy) % self.rows][(x + dx) % self.cols]
                    for dy in (-1, 0, 1)
                    for dx in (-1, 0, 1)
                    if not (dx == 0 and dy == 0)
                )

                if self.grid[y][x]:
                    new_grid[y][x] = 1 if alive_neighbors in (2, 3) else 0
                else:
                    new_grid[y][x] = 1 if alive_neighbors == 3 else 0

        self.grid = new_grid
        self.update()

    def clear(self):
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.update()

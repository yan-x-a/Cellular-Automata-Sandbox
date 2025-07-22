from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget
from base_widget import BaseAutomatonWidget

CELL_SIZE = 10
WHITE_COLOR = QColor(240, 240, 240)
BLACK_COLOR = QColor(40, 40, 40)
GRID_COLOR = QColor(200, 200, 200)
ANT_COLOR = QColor(200, 50, 50)  # Red ant

# Directions: 0 = up, 1 = right, 2 = down, 3 = left
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class LangtonsAntWidget(BaseAutomatonWidget):
    """Langton's Ant widget"""
    def __init__(self, rows: int = 120, cols: int = 190, cell_size: int = 10, parent=None):
        super().__init__(rows, cols, cell_size = 10, background_color=WHITE_COLOR, parent=parent)
        self.ant_x = cols // 2
        self.ant_y = rows // 2
        self.ant_dir = 0  # Facing up


    # rendering
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), WHITE_COLOR)

        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x]:
                    painter.fillRect(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                        BLACK_COLOR,
                    )

        # Draw ant
        painter.fillRect(
            self.ant_x * CELL_SIZE,
            self.ant_y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
            ANT_COLOR,
        )

        # Draw grid lines
        painter.setPen(QPen(GRID_COLOR))
        for x in range(self.cols + 1):
            painter.drawLine(x * CELL_SIZE, 0, x * CELL_SIZE, self.rows * CELL_SIZE)
        for y in range(self.rows + 1):
            painter.drawLine(0, y * CELL_SIZE, self.cols * CELL_SIZE, y * CELL_SIZE)

    # simulation
    def step(self):
        # Flip color
        current_color = self.grid[self.ant_y][self.ant_x]
        self.grid[self.ant_y][self.ant_x] = 1 - current_color  # Flip 0<->1

        # Turn
        if current_color == 0:
            self.ant_dir = (self.ant_dir + 1) % 4  # Right turn on white
        else:
            self.ant_dir = (self.ant_dir - 1) % 4  # Left turn on black

        # Move forward
        dx, dy = DIRECTIONS[self.ant_dir]
        self.ant_x = (self.ant_x + dx) % self.cols
        self.ant_y = (self.ant_y + dy) % self.rows

        self.update()

    def clear(self):
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.ant_x = self.cols // 2
        self.ant_y = self.rows // 2
        self.ant_dir = 0
        self.update()

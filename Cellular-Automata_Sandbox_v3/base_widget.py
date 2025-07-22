from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui     import QColor, QPainter, QPen

__all__ = ["BaseAutomatonWidget"]

class BaseAutomatonWidget(QWidget):
    """foundation for cellular-automaton widgets."""

    def __init__(
        self,
        rows: int,
        cols: int,
        *,
        cell_size: int = 10,
        background_color: QColor | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.background_color = (
            background_color if background_color is not None else QColor(255, 255, 255)
        )

        # grid and helpers
        self.grid = [[0] * cols for _ in range(rows)]  # subclasses can override
        self.drawing = False
        self.draw_state = 1  # subclasses decide what this means

        self.setFixedSize(cols * cell_size, rows * cell_size)
        self.setMouseTracking(True)

    # Convenience helpers
    def fill_background(self, painter: QPainter):
        painter.fillRect(self.rect(), self.background_color)

    def draw_grid_lines(self, painter: QPainter, grid_color: QColor | None = None):
        if grid_color is None:
            grid_color = QColor(200, 200, 200)
        painter.setPen(QPen(grid_color))
        for x in range(self.cols + 1):
            painter.drawLine(
                x * self.cell_size,
                0,
                x * self.cell_size,
                self.rows * self.cell_size,
            )
        for y in range(self.rows + 1):
            painter.drawLine(
                0,
                y * self.cell_size,
                self.cols * self.cell_size,
                y * self.cell_size,
            )

    def cell_at_pos(self, px: int, py: int):
        """Return the (x, y) cell indices for pixel coordinate (px, py)."""
        x = px // self.cell_size
        y = py // self.cell_size
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return x, y
        return None, None

    def cell_at_event(self, event):
        """Same as *cell_at_pos* but takes a QMouseEvent."""
        return self.cell_at_pos(event.x(), event.y())
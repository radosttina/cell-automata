class Dimensions:
    def __init__(self, xy, cell_width):
        self.x, self.y = xy
        self.width = cell_width
        self.rows = 0
        self.columns = 0
        self.padding_x = 0
        self.padding_y = 0

    def get_rows(self):
        self.rows = int(self.x // (1.5*self.width))
        self.padding_x = (self.x % self.rows) / 2 + (0.25*self.width)

        return self.rows, self.padding_x

    def get_columns(self):
        self.columns = int((self.y - self.padding_x) // (1.5*self.width))
        self.padding_y = (self.y % self.columns) / 2 + (0.25*self.width)

        return self.columns, self.padding_y

    def get_dimensions(self):
        return self.get_rows(), self.get_columns()
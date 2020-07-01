import pyglet
import numpy as np
from population_manager import Population
from dimensions import Dimensions
from screens.screen import Screen


class Game(Screen):
    def __init__(self, window):
        self.color_map = {
            0: [0, 0, 0],
            1: [72, 120, 140]
        }

        width = 6

        grid_params = Dimensions(window.get_size(), width)
        (self.dir_x_count, padding_x), (self.dir_y_count, padding_y) = grid_params.get_dimensions()
        self.population = Population((self.dir_x_count, self.dir_y_count))
        self.quads = self.calculate_quads(width, (self.dir_x_count, padding_x), (self.dir_y_count, padding_y))

        self.batch = pyglet.graphics.Batch()

    def initialize(self, **kwargs):
        self.population.initialize_population(**kwargs)
        pyglet.clock.schedule_interval(self.update, 1 / 12)

    def draw(self):
        self.batch.draw()

    def update(self, dt):
        self.batch.add(*self.get_quad_params(self.population))
        self.population.update_population()

    def calculate_quads(self, width, x_data, y_data):
        dir_x_count, padding_x = x_data
        dir_y_count, padding_y = y_data
        increment_x = 0
        increment_y = 0
        quads = []
        for i in range(dir_x_count):
            for j in range(dir_y_count):
                # this need to be one only on the first iteration
                new_quad = [padding_x + increment_x, padding_y + increment_y, padding_x + increment_x + width,
                            padding_y + increment_y,
                            padding_x + increment_x + width, padding_y + width + increment_y, padding_x + increment_x,
                            padding_y + width + increment_y]
                increment_y += width * 1.5
                quads.extend(new_quad)

            increment_y = 0
            increment_x += width * 1.5

        return np.array(quads)

    def get_quad_params(self, population):
        colors = []

        for i in range(self.dir_x_count):
            for j in range(self.dir_y_count):
                index = (i, j)
                color_key = population.get_unit_state(index)
                colors.extend(4 * self.color_map[color_key])

        return self.dir_x_count * self.dir_y_count * 4, pyglet.gl.GL_QUADS, None, ('v2f', self.quads), ('c3B', colors)

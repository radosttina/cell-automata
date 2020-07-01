import pyglet
import numpy as np
from population_manager import Population
from dimensions import Dimensions
from pyglet.window import key
import math
from screens.utils.label_manager import LabelManager
from screens.screen import Screen


class Canvas(Screen):
    def __init__(self, window):
        super().__init__(window)
        self.color_map = {
            0: [15, 15, 15],
            1: [255, 255, 255]
        }

        self.batch_content = None

        self.width = 6
        self.window = window

        grid_params = Dimensions(window.get_size(), self.width)
        (self.dir_x_count, padding_x), (self.dir_y_count, padding_y) = grid_params.get_dimensions()
        self.population = Population((self.dir_x_count, self.dir_y_count))
        self.quads = self.calculate_quads(self.width, (self.dir_x_count, padding_x), (self.dir_y_count, padding_y))

        self.batch = pyglet.graphics.Batch()

        self.help_label = LabelManager.getInstance().create_label('label',
                                                                  'Use mouse press/drag + SHIFT to draw. Use mouse press/drag + CTRL to erase.', 1, 'top')

        self.add_label_to_render_queue(self.help_label)

        @window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.handle_mouse_motion(x, y, modifiers)

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            self.handle_mouse_motion(x, y, modifiers)

    def initialize(self, **kwargs):
        self.population.initialize_population(pattern='canvas')
        pyglet.clock.schedule_interval(self.update, 1/12)

    def handle_mouse_motion(self, x, y, modifiers):
        cell_index = self.get_quad_index(x, y)
        if modifiers and modifiers == key.MOD_SHIFT:
            self.population.set_unit_state(cell_index, 1)
        elif modifiers and modifiers == key.MOD_CTRL:
            self.population.set_unit_state(cell_index, 0)

    def draw(self):
        self.batch.draw()
        super().draw()

    def delete_batch_content(self):
        if not self.batch_content:
            return

        self.batch_content.delete()

    def update(self, dt):
        self.delete_batch_content()
        self.batch_content = self.batch.add(*self.get_quad_params(self.population))

    def get_quad_index(self, x, y):
        cell_area = self.width*1.5
        index_y = int(math.floor(x / cell_area))
        index_x = int(math.floor(y / cell_area))

        return index_y, index_x

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

    def get_outbound_data(self):
        return {
            'prevent_next': False,
            'pattern': 'drawn',
            'canvas_data': self.population.get_raw_matrix()}

    def destroy(self):
        pyglet.clock.unschedule(self.update)
        self.delete_batch_content()

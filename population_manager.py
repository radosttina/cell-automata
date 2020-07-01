import image_conversion
import numpy as np
import copy


class Population:
    def __init__(self, xy):
        self.x, self.y = xy
        self.population = []
        self.modes = ['image', 'canvas', 'drawn']

    def initialize_population(self, canvas_data=None, pattern='image', image_location='', **kwargs):
        if pattern == 'image':
            self.population = image_conversion.get_binary_image(self.x, self.y, image_location)
        elif pattern == 'canvas':
            self.population = np.zeros((self.x, self.y))
        elif pattern == 'drawn':
            if type(canvas_data) == 'NoneType':
                canvas_data = np.zeros((self.x, self.y))
            self.population = canvas_data

        return self.population

    def get_supported_modes(self):
        return self.modes

    def set_unit_state(self, xy, state):
        self.population[xy] = state
        return self.population

    def get_unit_state(self, xy):
        return self.population[xy]

    def get_raw_matrix(self):
        return copy.copy(self.population)

    def update_population(self):
        new_population = np.zeros(shape=(self.x, self.y), dtype=int)
        for x in range(self.x):
            for y in range(self.y):
                state = 0
                for neighbor in [(x, y - 1), (x, y + 1),
                                 (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                                 (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]:
                    try:
                        state += self.population[neighbor]
                    except IndexError:
                        state += 0

                if self.population[x, y] == 1 and 4 > state > 1:
                    new_population[x, y] = 1
                elif self.population[x, y] == 0 and state == 3:
                    new_population[x, y] = 1

        self.population = new_population

        return self

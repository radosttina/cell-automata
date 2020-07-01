import pyglet
from pyglet.window import key
from screens.canvas import Canvas
from screens.image_choice import ImageChoice
from screens.screen import Screen


class Switcher:
    def __init__(self, window):
        self.window = window
        self.input_mechanism = None

    def get_keyboard_handler(self):
        self.input_mechanism.get_keyboard_handler()

    def initialize(self, **kwargs):
        if kwargs['pattern'] == "image":
            self.input_mechanism = ImageChoice(self.window, {})
        else:
            self.input_mechanism = Canvas(self.window)

        self.input_mechanism.initialize(**kwargs)

    def exit(self):
        return self.input_mechanism.exit()

    def destroy(self):
        return self.input_mechanism.destroy()

    def draw(self):
        return self.input_mechanism.draw()


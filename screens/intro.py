import pyglet
from screens.screen import Screen
from screens.utils.label_manager import LabelManager


class Intro(Screen):
    def __init__(self, window):
        super().__init__(window)
        welcome_label = LabelManager.getInstance().create_label('title', 'Game of Life', -5)
        self.add_label_to_render_queue(welcome_label)
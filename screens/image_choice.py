import pyglet
from pyglet.window import key
from tkinter import Tk
from screens.screen import Screen
from screens.utils.label_manager import LabelManager
import os

class ImageChoice(Screen):
    def __init__(self, window, config):
        super().__init__(window)
        self.window = window
        self.config = config
        self.pattern_index = 0
        self.title = LabelManager.getInstance().create_label('title', 'Enter the absolute path to the image...', -10)

        self.add_label_to_render_queue(self.title)
        self.setup_input_area(LabelManager.getInstance().font_size, window)

    def get_keyboard_handler(self):
        return self.caret

    def get_interaction_handler(self):
        def on_key_press(symbol, modifiers):
            if symbol == key.V and modifiers and modifiers == key.MOD_CTRL:
                self.document.text = Tk().clipboard_get()
                self.caret.position = len(self.document.text)

        return on_key_press

    def setup_input_area(self, font_size, window):
        self.add_label_to_render_queue(self.title)
        self.window.push_handlers(self.get_interaction_handler())
        self.document = pyglet.text.document.FormattedDocument(" ")
        self.document.set_style(0, window.width, dict(anchor_x='center', font_name='Roboto', font_size=font_size,
                                                      color=(255, 255, 255, 255), align='center'))
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, window.width,
                                                               window.height // 2 + font_size * 2, dict(align='center'))
        self.caret = pyglet.text.caret.Caret(self.layout, color=(255, 255, 255))
        self.caret.position = len(self.document.text)

    def draw(self):
        super().draw()
        self.layout.draw()

    def get_outbound_data(self):
        return {
            'prevent_next': not os.path.isfile(self.document.text),
            'image_location': self.document.text}


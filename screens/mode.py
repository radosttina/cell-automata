import pyglet
from pyglet.window import key
from screens.screen import Screen
from screens.utils.label_manager import LabelManager


class Mode(Screen):
    def __init__(self, window, config):
        super().__init__(window)
        self.window = window
        self.config = config
        self.pattern_index = 0
        self.title = LabelManager.getInstance().create_label('title', 'Choose the starting pattern...', -10)
        self.image_setup = LabelManager.getInstance().create_label('label', '> use image', -2)
        self.draw_setup = LabelManager.getInstance().create_label('label', 'draw pattern', 2)

        for label in [self.title, self.image_setup, self.draw_setup]:
            self.add_label_to_render_queue(label)

    def get_keyboard_handler(self):
        labels = [self.image_setup, self.draw_setup]

        def update_selection(direction):
            old_label = labels[self.pattern_index]
            old_label.text = old_label.text.replace("> ", "")
            self.pattern_index = (self.pattern_index + direction) % 2
            new_label = labels[self.pattern_index]
            new_label.text = "> " + new_label.text

        def on_key_press(symbol, modifiers):
            if symbol == key.DOWN:
                update_selection(1)

            if symbol == key.UP:
                update_selection(-1)

        return on_key_press

    def get_outbound_data(self):
        return {
            'prevent_next': False,
            'pattern': self.config['patterns'][self.pattern_index]}
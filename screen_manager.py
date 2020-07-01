from pyglet.window import key
from screens.utils.label_manager import LabelManager
from screens.intro import Intro
from screens.mode import Mode
from screens.game import Game
from screens.switcher import Switcher

FONT_SIZE = 16
PATTERNS = {'patterns': ['image', 'canvas']}

class ScreenManager:
    def __init__(self, window):
        self.window = window
        self.label_manager = LabelManager(window.width, window.height, FONT_SIZE)
        self.current_index = 0
        self.screens = [Intro(window),
                        Mode(window, PATTERNS),
                        Switcher(window),
                        Game(window)]

        window.push_handlers(self.get_keyboard_handler())
        self.screens[self.current_index].initialize()
        self.previous_state = {}

    def get_keyboard_handler(self):
        def on_key_press(symbol, modifiers):

            if symbol == key.ENTER:
                metadata = self.screens[self.current_index].exit()

                if metadata['prevent_next']:
                    self.window.clear()
                    self.screens[self.current_index].initialize(**self.previous_state)
                else:
                    self.current_index += 1
                    self.window.clear()
                    self.screens[self.current_index].initialize(**metadata)
                    self.previous_state = metadata

            if symbol == key.ESCAPE:
                self.window.close()

        return on_key_press

    def on_draw(self):
        try:
            self.screens[self.current_index].draw()
        except:
            self.window.close()

    def exit(self):
        self.window.pop_handlers()



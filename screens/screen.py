from screens.utils.label_manager import LabelManager


class Screen:
    def __init__(self, window):
        self.labels = []
        continue_label = LabelManager.getInstance().create_label('small_label', 'Press ENTER to continue...', -2, 'bottom')

        self.add_label_to_render_queue(continue_label)

    # helper methods
    def add_label_to_render_queue(self, label):
        self.labels.append(label)

    def get_keyboard_handler(self):
        return None

    def get_outbound_data(self):
        return {'prevent_next': False}


    # life-cycle methods
    def initialize(self, **kwargs):
        self.handlers = self.get_keyboard_handler()

        if self.handlers:
            self.window.push_handlers(self.handlers)

    def exit(self):
        self.destroy()
        return self.get_outbound_data()

    def destroy(self):
        self.handlers = self.get_keyboard_handler()

        if self.handlers:
            self.window.pop_handlers()


    def draw(self):
        for label in self.labels:
            label.draw()

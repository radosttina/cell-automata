import pyglet


class LabelManager:
    __instance = None
    @staticmethod
    def getInstance():
        if LabelManager.__instance is None:
            LabelManager()
        return LabelManager.__instance

    def __init__(self, ww, wh, font_size=16):
        if LabelManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LabelManager.__instance = self
            self.font_size = font_size
            self.ww = ww
            self.wh = wh

    def create_label(self, type, text, offset=1, position='middle'):
        adjusted_font_size = self.font_size

        if position == 'top':
            y_position = self.wh
        elif position == 'bottom':
            y_position = 0
        else:
            y_position = self.wh // 2

        y_position -= adjusted_font_size * offset

        if type == 'title':
            adjusted_font_size *= 1.5
        elif type == 'small_label':
            adjusted_font_size *= 0.75

        return pyglet.text.Label(text,
                          font_name='Roboto',
                          font_size=adjusted_font_size,
                          x=self.ww // 2, y=y_position,
                          anchor_x='center', anchor_y='center')

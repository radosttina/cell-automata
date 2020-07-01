import pyglet
from screen_manager import ScreenManager

window = pyglet.window.Window(fullscreen=True)
screen_manager = ScreenManager(window)

@window.event
def on_draw():
    window.clear()
    screen_manager.on_draw()

pyglet.app.run()
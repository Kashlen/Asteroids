import pyglet, math
from pyglet import gl
from pyglet.window import key

ROTATION_SPEED = 1 # radians per second ZKOUŠET
ACCELERATION = 30
WIDTH = 900
HEIGHT = 600

objects = []
game_batch = pyglet.graphics.Batch()
pressed_keys = set() # Vesmírná loď se 
                    # pak do množiny „podívá” v rámci své metody tick
dt = pyglet.clock.tick()

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


class Spaceship:
    def __init__(self):
        self.x, self.y = [WIDTH // 2, HEIGHT // 5]
        self.x_speed = 50
        self.y_speed = 50
        self.rotation = 1.5708
        image = pyglet.image.load("resources/blue_spaceship.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.sprite = pyglet.sprite.Sprite(image, batch=game_batch)

    def tick(self, dt):
        self.x = self.x + dt * self.x_speed * math.cos(self.rotation)
        self.y = self.y + dt * self.y_speed * math.sin(self.rotation)
        self.sprite.x, self.sprite.y = [self.x, self.y]   
        if "left" in pressed_keys:
            self.rotation = self.rotation + dt * ROTATION_SPEED
            self.sprite.rotation = 90 - math.degrees(self.rotation)
        if "right" in pressed_keys:
            self.rotation = self.rotation - dt * ROTATION_SPEED
            self.sprite.rotation = 90 - math.degrees(self.rotation)
        if "up" in pressed_keys:
            self.x_speed += dt * ACCELERATION
            self.y_speed += dt * ACCELERATION


def pressed_key(symbol, modifiers):
    if symbol == key.UP:
        pressed_keys.add("up")
    if symbol == key.LEFT:
        pressed_keys.add("left")
    if symbol == key.RIGHT:
        pressed_keys.add("right")

def released_key(symbol, modifiers):
    if symbol == key.UP:
        pressed_keys.discard("up")
    if symbol == key.LEFT:
        pressed_keys.discard("left")
    if symbol == key.RIGHT:
        pressed_keys.discard("right")

def draw():
    window.clear()
    game_batch.draw()





ship = Spaceship()
ship.__init__()

window.push_handlers(
    on_draw = draw,
    on_key_press = pressed_key,
    on_key_release = released_key,
)

pyglet.clock.schedule(ship.tick)
pyglet.app.run()
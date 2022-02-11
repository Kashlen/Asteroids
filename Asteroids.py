from random import randint, uniform, choice
import os
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


class SpaceObject:
    def __init__(self, x, y, rotation, x_speed, y_speed):
        self.x, self.y = [x, y]
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation

    def tick(self, dt):
        self.x = self.x + dt * self.x_speed * math.cos(self.rotation)
        self.y = self.y + dt * self.y_speed * math.sin(self.rotation)
        self.sprite.x, self.sprite.y = [self.x, self.y]   
       

class Spaceship(SpaceObject):
    def __init__(self):
        super().__init__(x=WIDTH // 2, y=HEIGHT // 5, rotation=1.5708, x_speed=50, y_speed=50)
        image = pyglet.image.load("resources/blue_spaceship.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.sprite = pyglet.sprite.Sprite(image, batch=game_batch)
        
    def tick(self, dt):
        super().tick(dt)
        if "left" in pressed_keys:
            self.rotation = self.rotation + dt * ROTATION_SPEED
            self.sprite.rotation = 90 - math.degrees(self.rotation)
        if "right" in pressed_keys:
            self.rotation = self.rotation - dt * ROTATION_SPEED
            self.sprite.rotation = 90 - math.degrees(self.rotation)
        if "up" in pressed_keys:
            self.x_speed += dt * ACCELERATION
            self.y_speed += dt * ACCELERATION

class Asteroid(SpaceObject):
    def __init__(self):
        super().__init__(x=0, y=0, rotation=uniform(0,6.3), x_speed=randint(20,50), y_speed=randint(20,50))
        images = os.listdir("resources/asteroid")
        png = choice(images)
        image_a = pyglet.image.load("resources/asteroid/" + png)
        image_a.anchor_x = image_a.width // 2
        image_a.anchor_y = image_a.height // 2
        self.sprite = pyglet.sprite.Sprite(image_a, batch=game_batch)


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

    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            # Remember the current state
            gl.glPushMatrix()
            # Move everything drawn from now on by (x_offset, y_offset, 0)
            gl.glTranslatef(x_offset, y_offset, 0)
    
            game_batch.draw()

            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()

ship = Spaceship()
asteroid1 = Asteroid()
asteroid2 = Asteroid()
asteroid3 = Asteroid()


window.push_handlers(
    on_draw = draw,
    on_key_press = pressed_key,
    on_key_release = released_key,
)


pyglet.clock.schedule(ship.tick)
pyglet.clock.schedule(asteroid1.tick)
pyglet.clock.schedule(asteroid2.tick)
pyglet.clock.schedule(asteroid3.tick)
pyglet.app.run()
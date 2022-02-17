from random import randint, uniform, choice
import os
from threading import Timer
from typing import overload
import pyglet, math
from pyglet import gl
from pyglet.window import key


ROTATION_SPEED = 1 # radians per second ZKOUŠET
ACCELERATION = 30
WIDTH = 900
HEIGHT = 600

objects = []
game_batch = pyglet.graphics.Batch()
pressed_keys = set() 
dt = pyglet.clock.tick()

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


class SpaceObject:
    def __init__(self, x, y, rotation, x_speed, y_speed, radius, laser_countdown):
        self.x, self.y = [x, y]
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation
        self.radius = radius
        self.laser_countdown = laser_countdown
        objects.append(self)

    def tick(self, dt):
        self.x = self.x + dt * self.x_speed * math.cos(self.rotation)
        self.y = self.y + dt * self.y_speed * math.sin(self.rotation)
        self.sprite.x, self.sprite.y = [self.x, self.y] 

    def delete(self):
        if self in objects:
            objects.remove(self)
        self.sprite.delete()

    def hit_by_spaceship(self, spaceship):
        pass

    def hit_by_laser(self):
        pass


class Spaceship(SpaceObject):
    def __init__(self):
        super().__init__(x=WIDTH // 2, y=HEIGHT // 5, rotation=1.5708, x_speed=50, y_speed=50, radius=40, laser_countdown=-0.1)
        image = pyglet.image.load("resources/blue_spaceship.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.sprite = pyglet.sprite.Sprite(image, batch=game_batch)

    def tick(self, dt):
        super().tick(dt)
        self.laser_countdown -= dt
        if "left" in pressed_keys:
            self.rotation = self.rotation + dt * ROTATION_SPEED
            self.sprite.rotation = 90 - math.degrees(self.rotation)
        if "right" in pressed_keys:
            self.rotation = self.rotation - dt * ROTATION_SPEED
            self.sprite.rotation = 90 - math.degrees(self.rotation)
        if "up" in pressed_keys:
            self.x_speed += dt * ACCELERATION
            self.y_speed += dt * ACCELERATION
        if "space" in pressed_keys:
            if self.laser_countdown < 0:
                Laser(self.x, self.y, self.rotation, self.x_speed, self.y_speed, self.radius, self.laser_countdown)
                self.laser_countdown = 2.5
        for object in objects:
            if overlaps(self, object):
                object.hit_by_spaceship(self)

class Laser(SpaceObject):
    def __init__(self, x, y, rotation, x_speed, y_speed, radius, laser_countdown):
        super().__init__(x=spaceship.x, y=spaceship.y, rotation=spaceship.rotation, x_speed=spaceship.x_speed+400, y_speed=spaceship.y_speed+400, radius=5, laser_countdown=0)
        image = pyglet.image.load("resources/laser.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.sprite = pyglet.sprite.Sprite(image, batch=game_batch)
        self.time_to_stay = 2  

    def tick(self, dt):
        super().tick(dt)
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        for object in objects:
            if overlaps(self, object):
                object.hit_by_laser()
        self.time_to_stay -= dt
        if self.time_to_stay <= 0:
            objects.remove(self)

class Asteroid(SpaceObject):
    def __init__(self, png):
        super().__init__(x=0, y=0, rotation=uniform(0,6.3), x_speed=randint(20,50), y_speed=randint(20,50), radius=0, laser_countdown=0)
        images = os.listdir("resources/asteroid")
        self.png = choice(images)
        image_a = pyglet.image.load("resources/asteroid/" + self.png)
        image_a.anchor_x = image_a.width // 2
        image_a.anchor_y = image_a.height // 2
        self.sprite = pyglet.sprite.Sprite(image_a, batch=game_batch)
        choose_radius = {"asteroid_l.png": 45, "asteroid_m.png": 18, "asteroid_s.png": 8}
        self.radius = int(choose_radius[str(self.png)])
        
    def hit_by_spaceship(self, spaceship):
        spaceship.delete()
    
    def hit_by_laser(self):
        asteroid_size = self.png
        self.delete()
        if asteroid_size == "asteroid_l.png":
            Asteroid(png="asteroid_m.png")
            Asteroid(png="asteroid_m.png")
        elif asteroid_size == "asteroid_m.png":
            Asteroid(png="asteroid_s.png")
            Asteroid(png="asteroid_s.png")
        else:
            pass


def pressed_key(symbol, modifiers):
    if symbol == key.UP:
        pressed_keys.add("up")
    if symbol == key.LEFT:
        pressed_keys.add("left")
    if symbol == key.RIGHT:
        pressed_keys.add("right")
    if symbol == key.SPACE:
        pressed_keys.add("space")

def released_key(symbol, modifiers):
    if symbol == key.UP:
        pressed_keys.discard("up")
    if symbol == key.LEFT:
        pressed_keys.discard("left")
    if symbol == key.RIGHT:
        pressed_keys.discard("right")
    if symbol == key.SPACE:
        pressed_keys.discard("space")

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


def distance(a, b, wrap_size):   # Distance in one direction (x or y)
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):   #Returns true iff two space objects overlap
    distance_squared = (distance(a.x, b.x, window.width) ** 2 + distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared

def tick(dt):
    for object in objects:
        object.tick(dt)


spaceship = Spaceship()
asteroid1 = Asteroid(png=0)
asteroid2 = Asteroid(png=0)
asteroid3 = Asteroid(png=0)


window.push_handlers(
    on_draw = draw,
    on_key_press = pressed_key,
    on_key_release = released_key,
)


pyglet.clock.schedule(tick)
pyglet.app.run()
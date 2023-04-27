import random

import numpy as np
import pyglet
from pyglet import window
from DIPPID import SensorUDP
from time import sleep


# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)


# window properties
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
LEFT_BORDER = 9
RIGHT_BORDER = 755
TOP_BORDER = 10
BOTTOM_BORDER = 585
SPACESHIP_SPEED = 2
SPACESHIP_HEIGHT = 48
SPACESHIP_WIDTH = 48
ROCKET_SPEED = 4
ENEMY_SPEED = 6
POINTS = 0

already_shot = False

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)


batch = pyglet.graphics.Batch()
background = pyglet.graphics.Group(0)
foreground = pyglet.graphics.Group(1)
# background img from https://unsplash.com/de/fotos/uhjiu8FjnsQ
background_img = pyglet.image.load('./sprites/background.jpg')
background = pyglet.sprite.Sprite(background_img, x=0, y=0, batch=batch, group=background)

score = pyglet.text.Label(text=f"Score: {POINTS}", x=LEFT_BORDER, y=BOTTOM_BORDER, batch=batch)


class Spaceship:
    # sprite downloaded from https://foozlecc.itch.io/void-main-ship
    def __init__(self, speed=10, img='./sprites/spaceship.png', x=50, y=50, group=foreground):
        self.speed = speed
        self.img = pyglet.image.load(img)
        self.spaceship = pyglet.sprite.Sprite(self.img, x=x, y=y)
        self.x = x
        self.y = y

    def move_x(self, move_right=False):
        if move_right:
            self.x += self.speed
        else:
            self.x -= self.speed
        self.spaceship.position = (self.x, self.y, 0)

    def move_y(self, move_down=False):
        if not move_down:
            self.y += self.speed
        else:
            self.y -= self.speed
        self.spaceship.position = (self.x, self.y, 0)

    def draw(self):
        self.spaceship.draw()


class Rocket:
    rockets = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = pyglet.shapes.Circle(self.x, self.y, 3, color=(255, 255, 0), batch=batch, group=foreground)

    def update_rockets():
        for rocket in Rocket.rockets:
            rocket.move()

    def draw_rockets(self):
        for rocket in Rocket.rockets:
            rocket.draw()

    def create_rocket():
        Rocket.rockets.append(Rocket(spaceship.x + (SPACESHIP_WIDTH/2), spaceship.y + (SPACESHIP_HEIGHT/2)))

    def move(self):
        self.y += ROCKET_SPEED
        self.shape.position = (self.x, self.y)

    def draw(self):
        self.shape.draw()

    def delete_rocket(self):
        Rocket.rockets.remove(self)
        self.shape.delete()


class Enemy:
    enemies = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = pyglet.shapes.Circle(self.x, self.y, 6, color=(255, 255, 255), batch=batch, group=foreground)

    def update_enemies():
        for enemy in Enemy.enemies:
            enemy.move()

    def draw_enemies(self):
        for enemy in Enemy.enemies:
            enemy.draw()

    def create_enemy(x, y):
        Enemy.enemies.append(Enemy(x, y))

    def move(self):
        self.y -= ENEMY_SPEED
        self.shape.position = (self.x, self.y)

    def draw(self):
        self.shape.draw()

    def delete_enemy(self):
        Enemy.enemies.remove(self)
        self.shape.delete()



spaceship = Spaceship(SPACESHIP_SPEED)


@win.event
def on_draw():
    win.clear()
    batch.draw()
    spaceship.draw()


def update(dt):
    global already_shot

    # check if the sensor has the 'accelerometer' capability
    if sensor.has_capability('rotation'):
        print(sensor.get_value('rotation'))
        # x rotation
        angle_x = sensor.get_value('rotation')['pitch']
        # y rotation
        angle_y = sensor.get_value('rotation')['roll']
        sprite_move(angle_x, angle_y)

    if sensor.has_capability('button_1'):
        button_value = sensor.get_value('button_1')
        if button_value == 1:
            if not already_shot:
                Rocket.create_rocket()
            already_shot = True

        if button_value == 0:
            already_shot = False

        if len(Rocket.rockets) > 0:
            Rocket.update_rockets()

    check_for_hit()
    spawn_enemies()


def check_for_hit():
    global POINTS
    rockets = Rocket.rockets
    enemies = Enemy.enemies

    for rocket in rockets:
        for enemy in enemies:
            # https://iq.opengenus.org/distance-between-two-points-2d/
            dist_x = rocket.x - enemy.x
            dist_y = rocket.y - enemy.y
            dist = np.sqrt(pow(dist_x, 2) + pow(dist_y, 2))
            if dist <= rocket.shape.radius + enemy.shape.radius:
                rocket.delete_rocket()
                enemy.delete_enemy()
                POINTS += 1
                # got score.text with ChatGPT Prompt
                score.text = f"Score: {POINTS}"


def spawn_enemies():
    randX = random.randint(10, 790)
    rand = random.randint(0, 100)
    if rand == 0 or rand == 50:
        Enemy.create_enemy(randX, BOTTOM_BORDER)
    if len(Enemy.enemies) > 0:
        Enemy.update_enemies()


def sprite_move(angle_x, angle_y):
    # for x movement
    if LEFT_BORDER < spaceship.x < RIGHT_BORDER:
        if angle_x < 0:
            spaceship.move_x(False)
        else:
            spaceship.move_x(True)
    elif spaceship.x < LEFT_BORDER + 1:
        spaceship.move_x(True)
    elif spaceship.x > RIGHT_BORDER - 1:
        spaceship.move_x(False)

    # for y movement
    '''
    if TOP_BORDER < spaceship.y < BOTTOM_BORDER:
        if angle_y < 0:
            spaceship.move_y(False)
        else:
            spaceship.move_y(True)
    elif spaceship.y > BOTTOM_BORDER - 1:
        spaceship.move_y(True)
    elif spaceship.y < TOP_BORDER + 1:
        spaceship.move_y(False)
    '''
        # angle_y = sensor.get_value('rotation')['y']
        # angle_z = sensor.get_value('rotation')['z']


pyglet.clock.schedule_interval(update, 0.01)

pyglet.app.run()


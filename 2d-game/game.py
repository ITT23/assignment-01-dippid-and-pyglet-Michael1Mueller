import random
import numpy as np
import pyglet
from pyglet import window
from DIPPID import SensorUDP
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, LEFT_BORDER, RIGHT_BORDER, BOTTOM_BORDER, TOP_BORDER
from constants import SPACESHIP_SPEED, SPACESHIP_HEIGHT, SPACESHIP_WIDTH
from constants import ROCKET_SPEED, ENEMY_SPEED, GAME_OVER_Y, GAME_OVER_X
from constants import LINE_HEIGHT, FONT_SIZE
from constants import batch, batch_game_over, background, foreground
from Enemy import Enemy



# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

status_running = True
already_shot = False
points = 0

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

# background img from https://unsplash.com/de/fotos/uhjiu8FjnsQ
background_img = pyglet.image.load('./sprites/background.jpg')
background = pyglet.sprite.Sprite(background_img, x=0, y=0, batch=batch, group=background)

score = pyglet.text.Label(text=f"Score: {points}", x=LEFT_BORDER, y=TOP_BORDER, batch=batch)

# text game over screen
game_over = pyglet.text.Label(text="GAME OVER", font_size=FONT_SIZE, x=GAME_OVER_X, y=GAME_OVER_Y, batch=batch_game_over,
                              group=foreground)

game_over_score = pyglet.text.Label(text=f"Your Score: {points}", font_size=FONT_SIZE, x=GAME_OVER_X,
                                    y=GAME_OVER_Y - LINE_HEIGHT, batch=batch_game_over, group=foreground)

restart_message = pyglet.text.Label(text="Press button_2 to restart or button_3 to quit", font_size=FONT_SIZE,
                                    x=GAME_OVER_X, y=GAME_OVER_Y - LINE_HEIGHT * 2, batch=batch_game_over,
                                    group=foreground)

# https://clipartcraft.com/download.html
explosion_img = pyglet.image.load("./sprites/explosion.png")
explosion = pyglet.sprite.Sprite(explosion_img, x=0, y=0, batch=batch_game_over,
                                 group=foreground)
explosion.scale = 0.3


class Spaceship:
    # sprite downloaded from https://foozlecc.itch.io/void-main-ship
    def __init__(self, speed=10, img='./sprites/spaceship.png', x=50, y=50, group=foreground):
        self.speed = speed
        self.img = pyglet.image.load(img)
        self.spaceship = pyglet.sprite.Sprite(self.img, x=x, y=y)
        self.x = x
        self.y = y

    def move(self, move_right=False):
        if move_right:
            self.x += self.speed
        else:
            self.x -= self.speed
        self.spaceship.position = (self.x, self.y, 0)
        explosion.position = (self.x, self.y, 0)

    def draw(self):
        self.spaceship.draw()


spaceship = Spaceship(SPACESHIP_SPEED)


# class structure inspiration from pyglet-demo (grips)
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
        # got .position with ChatGPT Prompt
        self.shape.position = (self.x, self.y)

    def draw(self):
        self.shape.draw()

    def delete_rocket(self):
        Rocket.rockets.remove(self)
        self.shape.delete()

    def delete_all():
        for rocket in Rocket.rockets:
            rocket.delete_rocket()


@win.event
def on_draw():
    win.clear()
    batch.draw()
    spaceship.draw()
    # only when spaceship is hit draw game over screen
    if not status_running:
        batch_game_over.draw()


def update(dt):
    global already_shot
    global status_running

    if status_running:

        # check if the sensor has the 'accelerometer' capability
        if sensor.has_capability('accelerometer'):
            angle_x = sensor.get_value('accelerometer')['x']
            sprite_move(angle_x)

        if sensor.has_capability('button_1'):
            button_value = sensor.get_value('button_1')
            if button_value == 1:
                # only shoot once per button click
                if not already_shot:
                    Rocket.create_rocket()
                already_shot = True

            if button_value == 0:
                already_shot = False

            if len(Rocket.rockets) > 0:
                Rocket.update_rockets()

        check_for_hit()
        check_for_crash()
        spawn_enemies()
        delete_elements_out_of_bounds()
    else:
        Enemy.delete_all()
        Rocket.delete_all()
        check_for_restart()


# deletes all enemies and rockets out of bounds
def delete_elements_out_of_bounds():
    for enemy in Enemy.enemies:
        if enemy.y < 0:
            enemy.delete_enemy()

    for rocket in Rocket.rockets:
        if rocket.y > WINDOW_HEIGHT:
            rocket.delete_rocket()


def check_for_restart():
    global status_running
    global points

    if sensor.has_capability('button_2'):
        button_value = sensor.get_value('button_2')
        if button_value == 1:
            status_running = True
            points = 0
            # got .text with ChatGPT Prompt
            score.text = f"Score: {points}"
            game_over_score.text = f"Score: {points}"

    if sensor.has_capability('button_3'):
        button_value_3 = sensor.get_value('button_3')
        if button_value_3 == 1:
            win.close()


def check_for_hit():
    global points
    rockets = Rocket.rockets
    enemies = Enemy.enemies

    for rocket in rockets:
        for enemy in enemies:
            # https://iq.opengenus.org/distance-between-two-points-2d/ for distance between 2 points in 2d
            dist_x = rocket.x - enemy.x
            dist_y = rocket.y - enemy.y
            dist = np.sqrt(pow(dist_x, 2) + pow(dist_y, 2))
            if dist <= rocket.shape.radius + enemy.meteor.width/2:
                rocket.delete_rocket()
                enemy.delete_enemy()
                points += 1
                # got .text with ChatGPT Prompt
                score.text = f"Score: {points}"
                game_over_score.text = f"Score: {points}"


def check_for_crash():
    global status_running
    enemies = Enemy.enemies

    for enemy in enemies:
        dist_x = spaceship.x - enemy.x
        dist_y = spaceship.y - enemy.y

        dist = np.sqrt(pow(dist_x, 2) + pow(dist_y, 2))
        if dist <= SPACESHIP_WIDTH/2 + enemy.meteor.width/2:
            enemy.delete_enemy()
            status_running = False


def spawn_enemies():
    # spawn enemies at random x location
    rand_x = random.randint(10, 790)
    rand = random.randint(0, 50)
    if rand == 0 or rand == 10 or rand == 25 or rand == 50:
        Enemy.create_enemy(rand_x, TOP_BORDER)
    if len(Enemy.enemies) > 0:
        Enemy.update_enemies()


def sprite_move(angle_x):
    # for x movement
    if LEFT_BORDER < spaceship.x < RIGHT_BORDER:
        # if spaceship is in bounds, move according to accelerometer data
        if angle_x > 0:
            spaceship.move(False)
        else:
            spaceship.move(True)
    # if spaceship gets out of bounds ->set back
    elif spaceship.x < LEFT_BORDER + 1:
        spaceship.move(True)
    elif spaceship.x > RIGHT_BORDER - 1:
        spaceship.move(False)


pyglet.clock.schedule_interval(update, 0.01)

pyglet.app.run()


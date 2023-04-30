import pyglet
from constants import ENEMY_SPEED, batch, foreground


# class structure inspiration from pyglet-demo (grips)
class Enemy:
    enemies = []

    # https://axassets.itch.io/spaceship-simple-assets meteaor sprite
    def __init__(self, x, y, img='./sprites/meteor.png'):
        self.x = x
        self.y = y
        self.img = pyglet.image.load(img)
        self.meteor = pyglet.sprite.Sprite(self.img, x=x, y=y, batch=batch, group=foreground)

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
        # got .position with ChatGPT Prompt
        self.meteor.position = (self.x, self.y, 0)

    def draw(self):
        self.meteor.draw()

    def delete_enemy(self):
        Enemy.enemies.remove(self)
        self.meteor.delete()

    def delete_all():
        for enemy in Enemy.enemies:
            enemy.delete_enemy()
